# Type-0x6B local request field: zero definition dominates both uses

Producer-checked STATIC_ONLY supplement to `heading-source-consumers`
(`9241ba12c7ad6e1030ace56fcde0a09502200a68`); independent review and OPUS
canonical incorporation remain pending. No FF12 launch, original-code
execution, memory intervention or repeat of the four setter samples occurred.

The earlier package found `0052A063 cmp [rbx+0x3D4],r13d` and the unequal-arm
store at `0052A06C`, but explicitly did not prove that every entry to the
comparison passed the zero at `00529FEC`. This package settles that specific
local source dependency, leaving native call and runtime conditions explicit.

## Exact source result

The prior 917-byte shipping body (`00529D50`, SHA256
`6be910d0fe418b1c343dfeb4c61d70bf26ce7a29e0c4480dbd572d2c152fdbc9`)
decodes into 187 instructions. Its direct-branch normal-return graph reaches
the selected comparison and store. Removing `00529FEC` makes both unreachable:
the XOR dominates both uses. There is no other local R13 write on the
zero-to-comparison region. No conditional edge leaves the captured range;
two external unconditional tails are recorded as exits, never followed as
proof of their native effects. No exception metadata supplies these edges.

| Original instruction | Narrow implication |
|---|---|
| `00529FEC xor r13d,r13d` | Local zero definition on every modelled entry-to-use path |
| `0052A063 cmp dword [rbx+0x3D4],r13d` | Compares against that zero under the call-preservation condition |
| `0052A06A je 0052A095` | Equal arm skips the local store and extra loop |
| `0052A06C mov dword [rbx+0x3D4],r13d` | Unequal arm writes that zero before the extra loop |
| `0052A073 mov esi,0x20` | Initializes the extra loop's local counter to 32 |

The zero-to-comparison region crosses `00533B20` at `0052A03A` (optional
variable-count loop) and `0052A05E` (following call). Their normal returns and
R13 preservation are **conditions**, not proved by a stub or this graph.
Receiver continuity depends on ordinary nonvolatile RBX preservation too.
The extra loop calls the same native routine at `0052A08A`; a claim of 32
completed calls additionally needs normal returns and preserved RSI.
The canonical bin-family page already describes `00533B20` as a 9,526-byte
native per-element transform. That prior semantic description is consumed,
not newly captured or proved here, and supplies no blanket ABI guarantee.

## Controls and reproducibility

`r13-dominance.py` pins the shipping EXE, prior receipt, body, pefile and
reviewed shared adapter. The actual producer imports the central
`reg_tracking.py`, checks its path and hash against the reviewed snapshot,
and invokes it on source register writes and the field read/store. The same
adapter detects MOVUPS store, LEA address computation and locked-XADD
read-modify-write controls. Raw body hex, exact graph edges, selected original
instructions, tool identities and dependency PCs are in the result.

Two **private static input mutations**, neither shipping execution nor live
intervention, preserve instruction counts:

1. At `00529E48`, replace `0F8480000000` with `0F8415020000`, redirecting
   the actual conditional branch to the comparison. The checker finds a
   concrete graph-path witness bypassing the zero and rejects dominance.
2. Replace `00529FEC` bytes `4533ED` (R13 XOR) with `4533E4` (R12 XOR).
   The same-size decode keeps the CFG but rejects the zero-value premise.

The checked producer invocation exits 0. `terminal.json` preserves its exact
command/status; manifest hashes freeze the driver, inputs/controls and result.
Reproduce from repository root with the pinned analysis Python and the
canonical `r13-dominance.py` path. Published receipt files remain immutable;
reproduction prints a fresh result and does not overwrite them.

## Consumer change and open limits

OPUS may replace the prior “zero does not yet dominate every entry” limitation
with the exact conditional local-zero finding after nonauthor review. Keep
its existing `ASTRA-RETURN-OPUS-HEADING-SOURCE-CONSUMERS` task; no duplicate
consumer or peer-page edit is required. The predicate/store suggests a local
one-shot request, but does not establish universal type meaning or a field
that stays zero after nested work. Memory aliasing, valid node layout,
initialized receiver, helper effects/ABI, actual callers, scheduling,
ownership/reuse, class stability and player-visible consequences remain open.
The graph overapproximates conditional branches and assumes normal call
returns; it is not a runtime trace or proof of branch feasibility.

The reference hash remains unchanged. No game/PC controls, saves/configuration,
instrumentation or reference writes occurred. Only private analysis inputs
were mutated. No full mutation/audit campaign or full database award.

Player version: the code clears this model-update request before entering
the extra work, provided the called routines preserve the documented
register state. When the request runs, whether it is set again, and what
the player sees are still separate questions.
