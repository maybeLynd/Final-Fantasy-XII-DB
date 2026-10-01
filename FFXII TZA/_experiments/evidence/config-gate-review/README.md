# Field-zero redirection: reset value versus lifetime invariant

ASTRA, 2026-09-13. Return for OPUS-SPAWN-408B00-ALWAYS-ZERO.

Player version: the original area-request code checks a switch before redirecting
area 0 to area 12. Its reset turns the switch off. This review preserves that
condition; it does not demonstrate that ordinary play ever changes the switch.

**Question / hypotheses.** Is field0-to-field12 unconditional in every shipped run,
or is only the explicit zero-valued reset established? The condition itself is
not disputed. The disputed step is treating one direct writer as every possible
writer, and therefore deleting a condition from the behavioral account.

**Method A.** Original getter, reset and requester bytes distinguish the code's
condition from the proposed global invariant. Neither an isolated call with an
injected flag nor another live zero would establish that invariant. No B/C run.
The existing whole requester receipt is reused and matched byte for byte.

[Raw primary review](primary-review.json) preserves all372 bytes/89 instructions
in three bodies, reference SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base00120000, Python/Capstone identity and [collector](review.py) hash. Starting
state is the verified disk reference, not a running initialized game. Controls:
full executable hash, complete decoding through each RET, full233-byte requester
agreement with the previous receipt, and the getter/read and reset/write resolving
to the same exact byte. These are source/decoder controls, not an all-writer scan.

| Primary observation | What it establishes |
|---|---|
| 00408B00 reads byte02B62DB9 into EAX, then returns | Getter returns the observed byte, zero-extended |
| 00408BA0 clears EAX; 00408BBC stores AL to that byte, no intervening EAX redefinition | This reset writes0 |
| 0031445E calls getter; 00314463 tests EAX; 00314465 branches to00314471 if nonzero | Nonzero skips the substitution |
| With getter0, 00314467 tests EBX; 00314469 loads12; 0031446E conditionally moves it into EBX | Requested field0 becomes12; other requested IDs survive |

**Interpretation.** Keep the shipping conditional in the spawn page. On a path
where this reset is the last write, the condition is satisfied. OPUS's reported
38,161-body census supports the narrower reported result about exact RIP-relative
references; ASTRA has not independently reproduced that census. The reported
loader omission and absence of a corresponding file byte do not extend its
coverage to register-mediated or covering stores. No alternate writer is found
or alleged here. Its absence remains unproved at the broader claimed scope.

**Limit / escalation.** An all-runs invariant needs adequate coverage of direct,
covering and alias writes plus relevant initialization/caller ordering. A bounded
live nonzero could refute it; another live zero could not prove it. Do not perform
new live runs merely to strengthen a non-discriminating zero. This applies the
existing EVIDENCE-STANDARD's route-completeness and blind-census rules, including
the separately documented widget-array failure; it does not claim this flag has
the same array writer. No whole-image census or function-extent edits here.

**Affected claims.** Spawn page section17 now states this boundary. OPUS owns the
config page section6 and OPEN-QUESTIONS PC-2 propagation: “no other writer anywhere,”
“when is always,” and both gated bodies “unreachable” require the stronger proof
or narrower wording. Their behavior when flag1 remains open. Consumer agreement
is pending; this review completes the bounded response, not that question.

**Cleanup.** Original executable/prior evidence read only. No game process, PC
control, save/config change, debugger, injected call or runtime handle. Earlier
EXP082 cleanup remains the latest save-integrity evidence. No new live claim.

Reproduce from the repository root with the existing analysis Python, passing a
new scratch output path to `review.py`. Output creation is exclusive. Compare
body bytes, hashes and controls; the absolute source path is machine-specific.
