# S33: initialized transform-history counters and their exact bounds

SOL in ASTRA, Method A STATIC_ONLY. Producer proof complete; independent review
and OPUS/FABLE consumption pending. No original-code execution or FF12 session.

The unresolved boundary was the `003FC170` call after the local visual updater.
Does its counter cap give safe bounds for arbitrary values, or does safety depend
on initialization and signed instruction order? Existing source and integer
induction suffice. New native samples or live absence sampling would not prove
the admitted range.

## Original identity and corrected stage name

Reference EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
preferred base `0x120000`. The actual capture uses the shared reviewed
`reg_tracking.op_kind` adapter; revalidation decodes every instruction through
that policy. `source-01.json` and terminal capture receipt preserve identity,
raw bytes, access annotations and the three adapter controls.

Five complete local bodies are retained: `003FC170..003FC3E2` (626 B),
`003FBE90..003FC16A` (730 B), `003FA160..003FA4D6` (886 B),
`00275550..0027556C` (28 B) and `00202C90..00202C97` (7 B). The proof pins
their hashes and closes their local CFGs; imports/callee effects remain qualified.

Manager source is reused from immutable packet commit
`045a4c6af279b2260989d523ee0edf96b81dcdc0`; its retained parent manifest and
member hashes are checked. This establishes input integrity, not independent
acceptance of the parent's semantics. No manager recapture or R7 rerun.

At `003FA801/805`, the manager passes **RCX = visual + 0x20** and **RDX = visual**.
Canonical `CONTRACT-per-frame-update-gate.md` and the existing EC-7 name identify
`003FC170` as the four-channel sinusoidal transform-history update. Calling it
the renderer or draw routine is imprecise. This is an additive correction to the
earlier packet's terminology; its conservative unclosed-callee limit remains
valid and published records remain immutable. These instructions do not prove
pixels were presented.

## Reset and initialized-range induction

On the successful source creation path, `003FA3EE/F3/F6` calls `00275550` with
the selected visual record and length `0x2A0`. For that positive length, the
original helper shifts the count right by two and zeroes `0xA8` DWORDs with
`REP STOSD`. This is the helper's exact source effect on valid writable memory,
not a stubbed effect. Later `003FA465` calls `003FBE90(visual+0x20,visual)`.
That initializer directly writes zero to the history counters in its four
iterations, conditional on normal returns and preserved nonvolatile registers.

The counters are DWORDs at visual offsets:

| Channel | Base | Counter |
|---|---:|---:|
| 0 | `+0x20` | `+0xA0` |
| 1 | `+0xB0` | `+0x130` |
| 2 | `+0x140` | `+0x1C0` |
| 3 | `+0x1D0` | `+0x250` |

In `003FC170`, original instruction order is:

1. `INC` the counter in memory, wrapping to 32 bits.
2. Load EBX; signed compare with 6; `CMOVGE` caps it to 6.
3. Store that value; `DEC EBX`, again wrapping to 32 bits.
4. Signed `JLE` skips shifting when the decremented value is nonpositive.
5. Otherwise copy one vec4 per iteration, decrementing to zero.

Starting in `0..6`, the stored result is in `1..6` and the number of shift
copies is `stored-1`, at most five. Thus `0..6` is inductive for the counter
transfer, provided other callees/writers do not change the counters. Four
channels are selected by the original loop bound; the apparent `index>=4`
input branch is not reached in that ordinary ABI-preserved four-iteration loop.

The complete `00202C90` is one 16-byte load followed by one 16-byte store and
RET. For channel base H and stored count n, shift destinations lie in
`[H+0x30, H+(n+2)*0x10)` and sources are 16 bytes earlier. The later latest-entry
copy writes `[H+0x20,H+0x30)`. Together with the explicit counter stores, these
sites lie inside `[H,H+0x84)`. Across four channels, the highest end is visual
`+0x254`, below phase `+0x260`, flags `+0x272` and links `+0x278/+0x280`.

This is the footprint of the **explicit stores and verified copy sites**.
It is not the composed footprint of every math callee. The source also calls
vector, matrix, normalization, heading and interpolation helpers with stack or
record destinations. Their output/no-alias contracts, normal returns and lack
of counter/control interference are explicit prerequisites to a wider theorem.
No whole-manager next-call release guarantee is awarded here.

## Exact malformed-state boundary

The signed counter cap is not safe for every 32-bit input. With initial
`INT32_MAX`, INC wraps to `INT32_MIN`; signed CMOVGE does not cap it. The negative
value is stored, then DEC wraps to `INT32_MAX`, so JLE enters the shift loop.
The nominal loop count is `2,147,483,647` under continued valid accesses/normal
returns. Its first addresses are already far outside the initialized history.

The neighboring `INT32_MAX-1` instead increments to INT32_MAX and caps to six,
giving five copies. Negative states other than that exceptional wrap skip the
shift until their counter progresses into the normal range. Five exhaustive
signed-32 intervals establish that INT32_MAX is the unique initial value with
this exceptional positive loop count.

This is a source/algebraic counterexample to an arbitrary-state bound. We did
not perform those accesses, provoke a crash, inject the value or prove natural
reachability. Shipped initialization and absence of later interference remain
the meaningful preconditions. Do not infer that ordinary play hits the boundary.

## Actual checks and reproduction

`proof-01.status.json` records terminal exit 0 with checked source prerequisites;
`result-01.json` preserves five closed bodies, 73 pinned instruction assertions,
seven normal-domain witnesses, five signed intervals and nine boundary witnesses.
These are proof/algebraic checks, not machine-code executions or game samples.

`control.py` requires that valid positive before invoking the actual proof CLI
on four labelled evidence defects: failed capture status, missing source, zero
bodies and changed retained parent. Each produces its expected diagnostic,
nonzero terminal exit, no result and empty stdout. Missing evidence cannot pass
as empty evidence. Inherited baseline hashes and each changed/missing input are
retained, so controls are reconstructible without duplicating their unchanged
inputs in the publication.

Run `prove.py` from the repository root with a fresh output path and `--src`
pointing to this packet, using the declared reference and Python/Capstone tools.
Included dependencies plus the pinned repository adapter are required. Existing
outputs are refused; published evidence must not be overwritten. The original
capture retains its owned-parent helper invocation; it was not rerun on sealing.

## Consumers and limits

OPUS: add the four counter offsets, initialized range, signed wrap precondition
and exact manager argument binding to the visual/history contract after review.
Preserve the distinction between local phase zero, occupancy clearing and unlink.
FABLE: refine renderer shorthand to transform history and retain sampled R7
timing limits. No new sprite/resource, allocator, scheduling or player-visible
effect claim follows.

The required wider gap is the remaining math-callee output/interference proof,
then any naturally initialized scheduling/drop/consequence observation still
required by the canonical question. Do not infer those effects from a stub or
from this integer transfer model. The 48–51 gameplay window remains unproved.

All our capture/proof/control children terminated. No PC control, game, service,
instrument, saves, configuration, reference bytes or peer work changed. Menu
allowance remains spent with extension unapproved; EXP127 remains invalid.
Goal ACTIVE/NOT_MET; required independent acceptance and full L1+L2 remain open.
