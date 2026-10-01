# Retry allocation is conditionally nullable in the local code

Player view: “retry allocation” does not mean this code must keep retrying until it succeeds. If the final allocation returns no block and both local retry conditions are clear, this routine takes its return path. This explains why the grid caller needs a successful-storage precondition or a separately proven stronger policy. It does not establish that gameplay reaches this path, runs out of memory, crashes or shows no dialog.

**Method A**, exact certified73461d shipping10B entry thunk0036A190,141B wrapper0036A1A0 and261B retry body0036BFE0. Two PE unwind-directory records corroborate the nonleaf source extents. Full instruction decode, original reader/shared reviewed operand-policy/driver/tool identities and consumer preimage are retained. No original, changed, native, emulator or live FF12 code was executed. Conditional predicate calculations are source controls, not eight gameplay or original-code tests.

Competing explanations:0036A190's EDX1 could force success-or-fatal; its retry could conditionally return null; or native callback/reclaim/allocator policy could prevent the local return. The original local code settles the first two at this boundary. The third remains unobserved and may restrict the source paths in actual initialized states.

0036A190 MOV EDX,1 then tail-jumps to0036A1A0. That wrapper saves the incoming flag in ESI and on its retry arm stores it at outgoing RSP+28 (sixth argument), with zero at+20 (fifth), then calls0036BFE0. After that callee's pushR14/sub20, its incoming fifth/sixth slots are at currentRSP+50/+58. Its complete exact body has no reads touching those slots and no local entry-stack address escape. This is a **local** unused-argument observation, not a claim that a native callee/callback never inspects a caller's stack. The incoming flag write alone does not prove a native fatal/no-null guarantee.

The retry routine invokes an optional callback and conditional reclaim operations, then the final allocator0036BC60 at0036C0A9. At the final decision diamond:

| final RAX | local EDI | local ESI | local outcome |
|---|---|---|---|
| nonzero | either | either | return epilogue0036C0CA |
| zero | zero | zero | return epilogue0036C0CA |
| zero | nonzero | either | retry backedge0036C013 |
| zero | zero | nonzero | retry backedge0036C013 |

EDI/ESI mean the low32 register state at that site. Callback-return/reclaim aggregation provenance is visible in source, but their native meanings/count domains and side effects are not proved. They are not invented initialized game values. The nullable exit leaves final RAX0 unchanged to RET0036C0E4. The allocation wrapper then tests that return and skips its header stamping on null. These original TEST/branch sites are counterexamples to the canonical memory page opening “never checks whether the memory ... arrived.” They do not prove every caller handles failure or that a particular OOM produces a visible outcome.

Discriminating control: one private source byte changes0036C0B9 JNE→JE with the same backedge target. Under finalRAX0/EDI0, the zero/nonzero ESI decisions both reverse. Original byte identity refuses that changed body. The success/nonzero outcome is the positive return control. Changed bytes are retained data only. Memory role assertions use the actual default shared reg_tracking.op_kind/written adapter, not raw Capstone access flags. The readonly checker re-derives exact source/extent/branch/stack identities without repeating an experiment.

Consumer implications: FABLE narrows the broad memory-page opening and OOM/player-outcome claims to what their actual evidence supports; preserve the original plus additive correction. OPUS records this nullable local domain and the unused local stack-flag boundary where it affects allocator/caller contracts. Navigation package47's lack of local null guard remains conditional: successful valid storage or a stronger **proved** native policy is needed; this package does not close actual native failure reachability. Arena selection push/pop preconditions are already documented and reused, not new locks/synchronization/lifetime guarantees or a whole allocator census.

Raw and normalized evidence, code/PE records/source identities, consumer preimage, controls, exact limits and readonly checker are retained. Independent SPEC review and canonical owners must agree before closure. No broader exports, general framework, shared consumer writes or cleanup of peer files.

Cleanup: image/reader/policy/peer sources read only; retained source mutation never executed/deployed. PC OFF, no game/process/input/memory/hook/save/config writes. Parked menu setup allowance spent and extension unapproved. Full L1+L2 remains NOT_MET. Learned next discriminator: determine real callback/reclaim/allocator policy and initialized state only if it materially blocks a consumer; do not rerun the settled final diamond or force a blind live OOM.
