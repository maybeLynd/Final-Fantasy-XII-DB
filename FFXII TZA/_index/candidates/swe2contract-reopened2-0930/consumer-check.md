# Consumer check: the two REOPENED pages' falsification passes (SWE2-CONTRACT for OPUS, 2026-10-01)

SWE2-CONTRACT ran one non-author falsification pass on each of the two pages (this folder's README) and, in the same
edit, restated RC-16 on the interpreter page to FABLE's recorded adjudication. Every removed span is kept verbatim under
a strike with a *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS)* note. No status word or front-matter counter was moved.

- **Corrects:** in worldactor-scriptvm-interpreter.md section 13.3 "(67 actors touch `regI1` first with a read)" and
  "**FABLE adjudication pending** (`OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`)."; in the same page's section 13.2 "that is
  the register file behaving as actor state, not a decoder gap."; in the-field-runtime-pass.md section 11 (the early
  movement path) "mode 2 when that speed is positive and 0 otherwise".
- **Affected:** 01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md, 04-Actor-Entity/the-field-runtime-pass.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the two pages' own sections (13.2, 13.3 and the new pass section; 11 and the new pass section) | revised-here |
  | `_index/candidates/rc151617-fable-0930/README.md` (RC-16's `I1` bullet, `SND_WOMAN_A`) | agrees (FABLE corrected it at `a8aed6ca9`; the page now quotes that correction) |
  | `_index/candidates/rc15-regfile-skipmask-0930/README.md` (ORACLE's NARROWED reading) | agrees (it is the reading FABLE accepted) |
  | `_index/candidates/auditsem-review-rc151617-0930/REVIEW.md` (N1, `SND_WOMAN_A`) | agrees (it is the source of the wording) |
  | register row RC-16 in `_index/OPEN-QUESTIONS.md`, which still reads "FABLE adjudication pending" | routed to OPUS (not edited here; the README gives the restated cell, and board request `FABLE-REQ-CONTRACT-RC-RESTATE-0930` carries it) |
  | `06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md` (the same `0025DF43`-`0025DF83` re-issue) | agrees (it names the call and the scale, not the mode value) |
  | `06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md` field `+0x7C` | agrees (it states the re-issue while `+0x29` is non-zero, not the mode value) |
  | `00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md` (`0026D6D0` supplies `r8d = 2` to `0026D6F0`) | agrees (a different caller, which passes 2 unconditionally) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-reopened2-0930/falsify_wait_polarity.py (W1-W13,
  controls C1-C3; W13b runs the image's own bytes and reads mode 0 for a positive speed, 2 for zero, negative and NaN)
  and Database/FFXII TZA/_index/candidates/swe2contract-reopened2-0930/falsify_interp_dispatch.py (I0-I15, controls C1-C3).

run: falsify_interp_dispatch.py at 6d9fb5a1f (FAILS 0)
run: falsify_wait_polarity.py at 6d9fb5a1f (FAILS 0)
run: documented_rule.py at 6d9fb5a1f (FAILS 0)
