# Procedural amplitude draw: mode-conditioned cost and corrected access metadata

**PASS_STATIC_ONLY — A. Zero new original-code executions or live runs.**
Complete003D8E50,418B, RET003D8FF1, body SHA
`32f4c93324e6c153518b5b42e85597f75495de8f66171fd58daf355e7b9a063a`;
shipping image73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Full raw instructions, original RIP targets, tool/reader identity and current
RNG-page preimage retained. EXP070/071 concern different helpers/init and were
neither rerun nor used to establish this helper's native callback effects.

The page's7steps-per-nonzero-call and14/28-step composed costs need their enabled
mode qualification.003D8E7D reads dword022D9138 **after** native call0036D930
at003D8E78, retaining the value in R8D. Both gates test this same latched register;
no intervening call reloads the mode. The original zero-mode JE003D8E8F skips
the five unrolled recurrences to003D8F36. JE003D8F7C skips the final two to003D8FC6.
The only own-body recurrence-state stores are003D8F26 and003D8FB8, at01EF93E8.
Neither is on that zero-mode path. Nonzero mode includes five then two operations,
committing after each block. This is seven operations, **not seven state stores**.

Ordered+0/-0 amplitude returns at003D8E6B before either native call or any global
write. The initial candidate that NaN would behave like zero is **refuted**:
UCOMISS003D8E5D is immediately followed by **JP003D8E60** to the nonzero path,
before JNE. The hypothesis is retained and stopped; no extra NaN experiment.
Floating-point exception controls and actual application amplitudes are unobserved.

Disabled nonzero calls are **not no-ops**. They reach the six own scratch writes
003D8F44/56/65/71/CD/D5 and the final native call0036D8E0 at003D8FE2. These copy/
scalar writes survive the recurrence gates. The first native call precedes the
mode latch and the final call follows the arithmetic; their native effects were
not executed or assumed inert. Consequently this packet proves own direct
recurrence cost conditional on the sampled mode, not that the entire invocation
leaves every other state unchanged.14steps-per-backend-rebuild or28-per-duplicate
apply additionally needs enabled mode at each latch and the callee/caller effects
and state assumptions justified independently. Normal reachability/order stays open.

The source check validates full body identity, zero/unordered branches, both mode
gates, the single latch, exact state/scratch write sites and five/two independent
mask/shift/bit-extract triples. Native boundaries stay explicitly excluded.

## Producer defect found and corrected

Capstone5.0.7 reports access flag READ for packed`MOVUPS [mem],xmm0` destinations.
The raw opcode is a **write**. Initial418B capture's provider flags, preserved in
`historical-capstone-access/source.json`, would omit003D8F56 and003D8FD5 as writes.
LEA's metadata also denotes address formation, not a memory read.

The corrected producer uses`operand_direction.py`'s restricted, explicit mnemonic/
operand roles for these two verified SSE bodies. It retains raw provider flags
separately and fails closed on unsupported forms. `check_direction.py` uses the
**actual shipping wrapper store**00202B86`0F1103` to reject the old classifier,
with original load00202B83 and LEA00202B79 controls. No bytes were executed or
recaptured to correct metadata; original body hashes remain unchanged.

The same defect exists in committed matrix packet58bd6303f's derived table:
00202B86 should be WRITE, and00202B79 address-only. The committed source and its
manifest are retained unchanged. `matrix-buffer-alias-access-correction.json`
is an **additive** normalized table. Any derived access footprint relying on the
two old rows is invalid until it uses the correction. The byte-based leaf-vector
snapshot/matrix-hazard and wrapper-copy proofs did not depend on those two labels
and remain valid; this is not a retraction of unrelated evidence or every Capstone
consumer. The historical immutable capture/check procedure is superseded for
access-role use by this corrected producer/regression; do not recapture it.

OPUS11504b7dd's plus4_check.py was inspected as a potential consumer: it parses
mnemonic/operand strings, does not enable Capstone detail/use`.access` flags, so
this flag defect does not directly invalidate that scan. This is a dependency
inspection only, not independent acceptance of its broader negative claim.
Other consumers need specific dependency checks, not a blanket waiver/retraction.

FABLE owns RNG/caller wording; OPUS types/contracts/access-footprint consumers;
SPEC independent source/correction review. Canonical propagation/review pending.
Stable source identity != live mode/scheduling/ownership proof. PC OFF; no game,
save/config/reference write or new cleanup receipt. Menu budget remains consumed,
additional recovery unapproved. Full accepted L1+L2/required audit goal NOT_MET.
