# Script array edge-clamp precondition — 69

**STATIC_ONLY.** Method A is sufficient for this claim. No FF12/native/VM or
isolated-original-code execution was performed. Conditional calculations are
labelled as such; they are not extra experiments or live observations.

Question: does `00262440` reject a zero dimension or require a nonempty dimension
for its documented edge-clamp behavior? Competing explanations were a rank guard
also guarding dimension values, a dimension-zero rejection in the clamp, or a
clamp stage that can compute -1 for a supplied zero dimension.

Exact retained shipping 591B source is verified byte-for-byte at the original65
commit and against its scientific-member hashes. The original strict47 publication
remains invalid; additive `b94b449ac08ffecde9c9045f984ab6f64c0b8db7` material recovery
applies. This package does not repair or overwrite that original manifest.
FF12 EXE SHA256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

The original header rank is `u16 +4`, subtracts one, sign-extends and uses `JS`
at `002624C0` to skip the entire dimension loop for rank0. A rank1 header enters
the loop regardless of its dimension value. The loop loads a **signed32** dimension
into ESI from `[RBP]` at `002624D5`. This differs from the unsigned16 rank/count.

At `0026250C..00262527`, with the original zero EBX preserved on the selected
integer-index and empty-stack routes, the sequence is:

```
TEST EAX,EAX; ECX=0; CMOVNS ECX,EAX       lower = index >= 0 ? index : 0
LEA EAX,[RSI-1]; CMP ECX,ESI; CMOVL      lower < signed_dim ? lower : low32(dim-1)
IMUL EAX,R8D; IMUL R8D,ESI; ADD R10D,EAX
```

Thus a strictly positive signed dimension clamps into `[0,dim-1]`. For dimension0
at this stage, any selected signed index gives lower>=0, the signed comparison
fails, and the predicted clamped value is -1. With initial product1/accumulator0,
the decoded contribution becomes -1 and product0. These are conditional static
consequences, not execution results. The stage contains no positivity rejection.
This does not rule out an upstream invariant or validation elsewhere.

Controls preserve full instruction bytes/operands, rank guard target, zero-register
preconditions, integer/empty-stack routes, and positive lower/upper edges for
dimensions1/5. A private **decoded-only** CMOVL→CMOVLE byte change is detected;
rank-versus-dimension and zero-as-edge checker faults reject. The capture and
checker actually invoke the direct compiled shared access adapter: the original
stack-depth store is `w`, dimension load `r`, LEA `addr`. No raw Capstone access
flags bypass the adapter. Default invocation reduces unchanged raw evidence.

Consumer change: qualify the edge-clamp statements in the variable-storage page,
array header/type documentation, contract and executable specification with a
**strictly positive signed32 dimension plus valid storage/state**. Preserve original
behavior for a supplied zero dimension if modelling this stage; do not add a native
validation/rejection or claim no fault for all malformed arrays. FABLE/OPUS/DATA
own their consumers; SPEC independent review then owner adjudication remains pending.

Still open: actual shipping dimension validity, upstream acceptance/rejection,
full resolver banks/addressing/access consequences, overflow/storage validity,
native faults, initialization/lifetime/reachability, and rank0 complete outcome.
No assets were censused. No live reads/interventions/processes/saves/configuration
or reference binary changes. PC control remained off; S19 spent budget and
unapproved extension persist. Full L1+L2 DB_GOAL=NOT_MET.
