# S33: retirement preserves the phase; release is a separate pass

SOL in ASTRA; producer evidence, independent acceptance pending. Method A,
STATIC_ONLY. No new original-code execution, FF12 process, PC control or game
input. This packet narrows the prepared S33 visual-slot question; it does not
close natural slot exhaustion, gameplay timing or consequences.

## Question and competing explanations

Does the retained R7 observation of release on update 51 prove a fixed clock
starting at neutral retirement? Or does retirement preserve the current phase,
with release requiring phase progression and a separate manager pass?

The original instructions settle the local protocol. A new game session or
repetition of the five R7 samples would add no distinguishing evidence to that
question. Real initialized values, caller cadence, interleaving and renderer
effects remain separate propositions.

## Identity, inputs and reproducibility

Reference: `FFXII_TZA.exe`, preferred base `0x120000`, SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
`source-01.json` retains complete bytes, instruction annotations, image/tool
identity and successful shared-adapter controls for these bodies:

| Body | Exclusive end | Bytes | Role |
|---|---|---:|---|
| `003FA820` | `003FA900` | 224 | Neutral retirement |
| `003FC510` | `003FC8FD` | 1005 | Local visual update |
| `003FA790` | `003FA81F` | 143 | Manager traversal |
| `003FA4E0` | `003FA567` | 135 | Unlink and clear |
| `001EDE80` | `001EDEBD` | 61 | Render gate |

`capture.py` invokes the reviewed capture helper. Its actual memory annotation
path uses `reg_tracking.op_kind`; the validator re-decodes every retained
instruction through the same reviewed access policy. Included dependencies and
the required repository adapter are pinned in `external-dependencies.json`.
The finite decline constant at `00D1204C` is separately read from the same
hashed image: bytes `000000c5`, binary32 `-2048.0`.

From the repository root, with the declared Python/Capstone dependencies and
reference image, run the packet's `prove.py` with a fresh output path and
`--src` pointing to this packet. Existing result identities are refused. The
three admission fixtures can be recreated from their receipts and retained
baseline files. Do not overwrite the published controls/results.

`proof-03.status.json` and stdout establish a terminal successful producer run:
five closed local CFGs and 75 pinned instruction assertions. These counts are
proof checks, not original-code executions or independent acceptance.
`proof-01` and `proof-02` failed during producer development because the shared
CFG helper returns `(pc, target_string)` call tuples. Both failures, their
stderr and driver preimages are retained. They produced no accepted results.

## Established local protocol

With valid record memory, ordinary ABI and no interfering writes, neutral
`003FA820(h,0)` on an occupied, not yet retired record with flag 8 clear:

- sets retired bit 1 in the word at `+0x272`;
- resets `+0x290` and `+0x294` to zero;
- preserves phase `+0x260`, motion `+0x264` and fade word `+0x270`;
- has no callee effects on that conditioned path.

`003FC510` chooses one phase handler per invocation. Phase 1 follows motion
and floating-point predicates and can become phase 2. A retired phase 2
becomes phase 3; with mode `+0x290=0`, it also clears flag `0x20`. Phase 3 can
become phase 0 only when the signed fade word is nonpositive after the earlier
fade update. A phase-2-to-3 store cannot reach the phase-3-to-0 store in the
same invocation. All direct local flag writes preserve occupied bit 0.

`003FA790` performs its phase-zero recycling pass **before** its local-update
pass. It saves `next` at `+0x278` before clearing/unlinking a phase-zero slot,
so the cleared links do not prevent traversal to another phase-zero slot.
`003FA4E0` clears links, flags and phase. Thus phase zero, clearing occupancy
and unlinking are distinct events. A phase-zero store in the second pass is
later than that invocation's first recycling pass.

This does **not** prove a whole-manager next-call guarantee. After the updater,
the manager tests `001EDE80` and can call `003FC170`. The gate's default branches
return 1. Rendering and other writers cannot be silently treated as inert.

## Discriminating invariant, not a sampled trajectory

Repeated local `003FC510` calls admit this conditional fixed point: phase 3,
flags 3, `0 < signed word +0x270 <= 0x4000`, mode `+0x290=0`, global frame-step
`01DFE0BC` equal to positive or negative zero, valid memory/ABI, no interfering
writes and ordinary masked floating-point exceptions.

The original instruction sequence is preserved: `MULSS` by the verified
finite `-2048.0` produces signed zero; `CVTTSS2SI` produces integer zero; adding
its low word preserves positive fade. The phase-zero store is skipped, as are
the mode-dependent application calls. Phase and occupied/retired flags remain
unchanged. This is a source-derived induction over the admitted local domain,
not a native fixture or a naturally reached state. It refutes a universal
51-local-call bound over that domain. It does not prove that shipped gameplay
can retain this zero-step state, nor what the renderer or elapsed game time does.

The retained peer `R7` result reports five retired slots freed on manager update
51, with slots 5–12 still live and no reported halt. That observation remains
valid within its fixture. The aged 48-update probe is README prose only in the
retained record, not a separately captured raw result. Neither is our new run.
Do not replace the floating-point sequence with real-number algebra or infer a
fixed lifetime from the observed values.

## Controls and producer-path defect

`control.py` executes the actual proof CLI with a required valid positive and
three labelled prerequisite defects: failed upstream capture status, missing
source and zero original bodies. Each refuses with its specific diagnostic,
nonzero terminal exit, empty stdout and absent result. A zero-case run is not a
pass. The invocation path checks upstream exit, terminal state, exception,
driver identity, stdout/stderr, source population, bytes and access roles.

The retained OPUS S33 driver imports its upstream `check` under redirected
stdout, then uses `C.W/C.uc/C.S` without checking `C.allok/C.results`. The exact
four-statement import prefix is extracted from the retained producer AST in
`import-controls-01/original-prefix.py`. Labelled host modules demonstrate:

| Upstream control | Prefix outcome |
|---|---|
| Nonempty passing verdict | Returns normally |
| Nonempty false verdict and printed FAIL | Returns normally; FAIL is hidden |
| Raised qualified exception | Does not return; child records exit 2 |

This demonstrates a missing verdict guard at the **real import stage**, not a
whole-native-suite false pass. The current retained upstream result reports
`ok=true` with four rows. This defect does not establish that the historical
R7 run had an upstream failure or refute all its observations. OPUS owns repair:
require checked nonempty upstream results and successful verdict/input identity
before downstream native state is used; preserve false/missing/exception
diagnostics. After repair, re-review that concrete path with a valid positive.

The initial import-control launcher failed with a syntax error before running
fixtures. Its terminal receipt/stderr and driver preimage are retained. The
corrected `import-control-02` is the accepted controller receipt; there are only
three executed host-prefix cases. No full native or mutation campaign was rerun.

## Consumers, remaining evidence and cleanup

OPUS owns the visual-record contract and the producer repair. FABLE owns loot
and presentation semantics. An independent SPEC review is required before the
new theorem is canonical. Existing S33 peer review is preserved and does not
automatically accept this packet or the import guard.

For the outstanding natural exhaustion question, record initialized phase,
motion, fade, flags, mode and frame step, and distinguish manager recycle pass
from local update and renderer. The normal chain remains: actual drop -> visual
creation -> any zero handle -> actual next pool tick -> observed consequence.
There is no proven gameplay fixed window of 48–51 updates. Prepared save/area,
first-visual state and positive detection controls remain missing. The parked
menu attempt's spent allowance and unapproved extension still apply.

No FF12 process/instrumentation or PC-control session was started. No saves,
configuration, reference binaries or peer files changed. All our bounded
helpers terminated, with terminal receipts. Goal ACTIVE/NOT_MET; natural
timing/reachability/consequence and required project reviews remain open.
