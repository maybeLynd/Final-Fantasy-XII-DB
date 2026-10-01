# Recursive status call: fresh mask-bit indices, not inherited outer id

The prior STRUCT caller-cone line for `0030E6C7` says its `movzx r8d,dil`
inherits the outer R8B saved at `0030E391`. **Original code resets EDI before
that call and iterates the bits of a DWORD mask.** Whenever this loop reaches
the recursive call under its valid-state/normal-ABI premises, R8B is 0..31
independently of the outer byte. This is a producer proof awaiting independent
review and canonical consumption, not a generic callee or full-system safety
claim.

Question/hypotheses: is the incoming outer id forwarded, or does the recursive
caller select a new bit index? Method **A** is sufficient: initialization,
increments, branch bounds and argument production are bounded original code.
It needs no natural initialized metadata sample, forced call, isolated execution
or live game. Those methods would add no evidence needed for this local invariant.

Reference EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base0x120000.
Capture includes 215 original bytes: `0030E360..0030E395` and
`0030E645..0030E6E7`. These are bounded fragments, **not** a complete callee CFG.
Actual Capstone5.0.7 and reviewed shared store/LEA/RMW access roles are used.
The final checker requires terminal successful capture and exact driver/source
bindings, re-decodes bytes, and compares every captured byte to the shipping EXE.

The loop's original sequence is:

| Source | Effect |
|---|---|
| `0030E682` or `0030E686` | Zero EDX on the two local join paths. |
| `0030E68A..0030E693` | Read/store DWORD metadata mask; zero mask skips the loop. Valid row memory is required. |
| `0030E69A` | `mov edi,edx` resets the loop counter to zero. |
| `0030E6A3/6A6` | Test mask bit EDI; clear bit skips the recursive call. |
| `0030E6B9/6C7` | Zero-extend DIL into R8D and call `0030E360`. |
| `0030E6CC/6D0` | After a normal return, reload the saved mask and zero EDX. |
| `0030E6D2..6D7` | Increment EDI, compare it with 0x20 and signed-JL back. |

Only initialization and increment directly write the counter in that loop.
Its one call requires ordinary nonvolatile-EDI preservation and backed/stable
caller frame as appropriate. Start0 and increment1 admit precisely 0..31 at
the argument site; increment from31 produces32 and exits, with no wrap reached.
The 32 arithmetic states in the result are a bounded induction check, **not
32 original-code executions**. A conditional mask0x10 with outerbyte31 would
call with argument4, refuting inheritance. It does not prove a natural shipped
resource has that mask or that the branch actually occurs during gameplay.

The actual positive capture/proof complete. Three synthetic regressions exercise
the real final CLI: failed capture status, coherent changed loop bound32→64,
and missing loop fragment. All refuse with the expected error and no result.
Their outputs establish producer detection, not native effects or independent
acceptance. No unchanged status sample, broader caller census or earlier
EXP-127 tracing is repeated.

Reproduce in this directory with the project's existing Python and fresh outputs:

    python prove-status-recursion-index-bound.py . status-recursion-index-bound-capture-01.status.json NEW_RESULT.json
    python control-status-recursion-index-bound.py NEW_CONTROL_DIRECTORY

The original-byte collector can be rerun from its owned ASTRA preparation
directory with the same EXE/dependencies. Existing input/result/receipt paths
must stay immutable; copied dependencies are identity receipts, not replacements
for the shared reviewed adapter.

STRUCT's recursive caller line should read “fresh bounded DWORD-mask bit index”
after independent acceptance. That strengthens the caller bound while correcting
the mechanism. FABLE/OPUS must distinguish it from the separate
`ov58d-order-switch` correction of the two false message-arm assignments.
Both are needed before removing the relevant region-A caller uncertainty, but
neither alone closes all external callers, state aliases or required OV-5/8
claims. Original cone history is retained; no peer-owned page is edited here.

Remaining premises: local entry through the zeroing joins; valid metadata row
and mask; normal callees preserve nonvolatile counter/frame state; no interfering
writes to relevant locals. Omitted full-function initialization, resource binding,
row address narrowing, exception behavior, arbitrary higher outer inputs,
natural recursion, transitive side effects, ownership/lifetime and presentation
remain unproved. This is no arbitrary-input sanitizer.

Cleanup: all finite children terminate, the reference image and adapter remain
unchanged, and no game/PC controls, native instrumentation, saves, configuration
or peer processes were started or modified. Full L1+L2 goal ACTIVE/NOT_MET;
parked menu allowance remains spent with extension unapproved and EXP-127
remains INVALID_POST_TRACE. Once delivered, continue the next independent
required question while review waits; do not re-test this settled loop.
