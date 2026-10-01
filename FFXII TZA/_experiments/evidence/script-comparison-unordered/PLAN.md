# ScriptVM three-way unordered comparison — candidate 77

Question: what three-way result does original25D740 produce for unordered float
operands, and how do six interpreter comparison opcodes consume that result?
Major system ScriptVM comparisons; semantic consumer FABLE, typed/ABI OPUS,
executable specification DATA/CONTRACT, independent SPEC review.

Existing pages settle identity, six callers, typed-pop layout and describe the
integer/float paths, but do not state unordered float outcomes. Do not replay
that answered identity census. Hypotheses: unordered propagates a distinct code,
falls through an equality result, or takes one of ordered comparison branches.

Choose A first for exact original source/consumer branch reasoning; select B
only if actual bounded effects/flags need a discriminator. Do not choose live:
this question is local instruction semantics under explicit operand/MXCSR state.
Read the complete verified shipping body, validate call boundaries and caller
result use before designing a harness. Reuse certified reader/shared adapter and
existing guest recipe if needed; no generic platform. At most finite ordered/
equal/NaN controls sufficient for selected claim; stop if detection/source/state
fails. Native exception flags/game RC/actual authored NaN reachability remain
open. No callback stub proof or full interpreter/game execution.

PC OFF; parked S19 method and spent budget persist; full L1+L2 NOT_MET.

Prepared source now distinguishes a masked unordered path: UCOMISS25D8B2,
JP25D8B5/JNE25D8B7 ->25D8D0; then COMISS25D8D3 and CMOVA25D8D6 select a result
from EDI initially1. Six original24-byte consumers at25EA18..25EA90 apply
SETE/SETNE/SETG/SETS/SETNS/SETLE after TEST EAX. Choose B for actual bounded
return/depth/write/branch effects, A for these source consumers. Run full413B
entry25D740 for initialized depth2/tag2 operands under masked MXCSR1F80; reject
any CALL (fault reporting is not stubbed). Finite less/equal/greater controls
must succeed before qNaN-left/right/self, then one labelled private JP->NOP
control must change unordered return to0. At most128 instructions per guest,
only depth/frame writes, original bytes/stack buffers/nonvolatile registers/RET
checked. Observe guest flags; do not equate them with native exception/status
behavior. No full interpreter/caller/live or authored NaN claim.

Reuse reader __file__/no bytecode/actual stdlib import controls learned70/72/76.

First capture invocation completed all seven bounded guests/RET/cleanup but then
failed because check.py had not yet been written. That invocation is INCOMPLETE,
not PASS. Preserve its exact executed driver/raw; reduction of retained evidence
must be a separate successful default invocation, with controls, no guest replay.
Producer now requires a present compilable checker before image/guest preparation;
write the checker before invoking later capture helpers. No accepted conclusion
depends on the missing-checker invocation being a successful pipeline.
