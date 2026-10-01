# Mixed ScriptVM comparison precision — candidate 78

Question: are integer and mixed-tag comparisons equivalent around2^24, or does
the both-int fast path preserve distinctions lost after promotion to float32?
Major system ScriptVM typed comparison; FABLE semantic and OPUS contract owners.

Choose **A** first: full original25D740 type-dispatch/conversion/comparison source,
retained72 original positive conversion results at actual c4cbbfb8, and existing
source six boolean consumers. Both-int1,1 branch bypasses CVTDQ2PS; mixed1,2
promotes integer through MOVD/CVTDQ2PS. Conditional comparison of16777217 versus
16777216 differs if the thread's rounding mode changes. Use exact retained bits
and source order, not a reconstructed fixture matching itself. No new positive
conversion replay or guest setup unless existing evidence cannot discriminate.

Controls: both integers versus mixed tags with the same numeric pair; RN versus
RU retained conversion bits; exact value below2^24 as type-independent control.
Explicitly label source predictions rather than original comparator execution.
Keep72 initial-label additive/source-derived limitation and masks/tool identity.
Do not inherit77 qNaN observations as mixed-path observations. Current claims
must be checked; no peer canonical consumer edits. Actual authored values/caller/
game RC/native flags/live remain open; full L1+L2 NOT_MET/PC OFF/S19 persists.

Reusable preconditions: checker must exist and compile before source preparation;
do not name a helper inspect.py (stdlib shadow). Use actual reviewed op_kind/
written adapter in capture AND reduction; store/read/LEA and private RMW controls.
Verify copied72 inputs against c4cbbfb8 and their manifest; keep initial-label
additive source/invocation-derived correction with the observed conversion bits.
This conditional composition settles the named discriminator without repeating
72 conversion guests or77 NaN guests. It is not actual mixed comparator execution.
