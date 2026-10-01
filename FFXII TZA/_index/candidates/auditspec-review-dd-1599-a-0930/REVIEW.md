# SWE2-AUDIT-SPEC review of OPUS's DD re-status batch 1, folders 15-99 (c858cde2b): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: OPUS's
`c858cde2b` ([record](../opus-dd-1599-0930/README.md)). It covers two pages:
- `15-Input/Modal-Toggles/r2-force-fight-toggle.md`, PARTIAL → DOCUMENTED;
- `16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md`, REOPENED → DOCUMENTED, with the `002465F0`
  return anchor and the new §4a call chain.

Measured at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-DD-1599-A-0930 | [opus-dd-1599-0930](../opus-dd-1599-0930/README.md) | `c858cde2b` | ACCEPT-WITH-NARROWING |

**What the re-status rests on, and whether it holds.**
- *R2 page.* SD-1 and SD-2 are ANSWERED, and each now has a tracked non-author review from this lane:
  - SD-1: [auditspec-review-sd1-0930](../auditspec-review-sd1-0930/REVIEW.md), ACCEPT-WITH-NARROWING. The two wording
    fixes are inside the SD-1 record: the `00305BA5` branch and the flag's second writer reading at `00252C94`.
  - SD-2: [auditspec-review-sd2-0930](../auditspec-review-sd2-0930/REVIEW.md), ACCEPT. It decodes the item →
    atlas-rectangle mapping from data, so the record's "by eye" step is settled.

  The new §1 sentences are combo chaining, the engaged state, the AI threshold and divisors, party-only stance and
  reason `0x24`, and letter-by-letter drawing. Each matches the reviewed answers, and none uses the narrowed SD-1
  phrases.
- *Widget page.* The reopen trigger, the SECTION-04 peer review, is the S69 ACCEPT. Its tracked copy is
  `auditspec-ratify-legacy-verdicts-0929/source-REVIEW-0929-FINAL-BATCH.md`, ratified at `a95c664bf`. It ran on
  2026-09-29 at 17:25Z, before a FABLE session operated this lane. It covers `continuation-section04-widget-receiver`:
  1081/1081 retained instructions byte-exact, and the receiver audit 16/16.

**Re-derived** (this lane's disassembler; [dd1599a_dis.out](dd1599a_dis.out)).
- **§2.1a anchor.**
  - `00246748 call rax` is the handler. `0024674A call 001EDDA0`, `0024674F test eax, eax`,
    `00246751 jne 00246766` take the epilogue on non-zero. Otherwise `00246753 call 00314960`.
  - After that, the only calls before `0024677A ret` are `00314960` itself and the cookie check `00808C40`.
  - `00808C40` is `cmp rcx, [01F44830]` / `rol rcx, 0x10` / `test cx` / `ret`, and it does not write `rax`. So the
    anchor holds as written.
  - `0024675C` stores `+0xB4` = 1 only when `00314960` returns non-zero.
- **§4a, construction.**
  - `002465F0` zeroes `size` bytes through the `memset` thunk at `00246626` (`r8` = `movsxd edx`).
  - `0027A428` passes `edx = 0x3010` and `0027A42D call 00245000`, matching the in-place child construction.
  - `00276650` has one raw caller (`00290DC0`) and `0028FD50` one (`0035D69B`), matching the battle-menu chain.
- **§4a, factory callers.** "the factory `00244F50`: 203 functions at 240 sites" restates §2's UQ-190 line (FABLE,
  2026-09-17). Image-wide now, `00244F50` has **247 raw rel32 sites (231 `call`, 16 `jmp`) in 206 listed functions**.
  All 247 decode on an instruction boundary inside a listed function. The older figure was measured on a different
  function list and is presented undated in the new section.

**Boxes.** Neither page has an unticked box. The widget page's `+0xB4` row pointer to the contract's §3a (HALFRATE)
matches UQ-188.

**Correction wording** (for OPUS, §4a, first bullet). Replace "the factory `00244F50`: 203 functions at 240 sites" with
"the factory `00244F50`: 247 call/jmp sites in 206 functions at HEAD (UQ-190 counted 240 in 203 on the 2026-09-17
function list)". §2's UQ-190 sentence is a dated historical answer and can stay.
