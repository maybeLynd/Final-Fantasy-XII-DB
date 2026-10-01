# Original GS coordinate conversion — bounded evidence plan

QUESTION: Does byte `01FD3611` only select coordinate decoding, or also bypass
the packed-path depth bounds? What exact vector, matrix/division, colour and UV
writes compose the vertex, and is the floating-point operation order relevant?

Consumer: FABLE's current Legacy-PS2-GS/the-vif1-vu1-layer.md §2.1b; OPUS's
width/layout/ABI qualification. This is a representation question for L1/L2,
not a renderer implementation or native parity campaign.

Hypotheses: both formats clamp Z versus only packed input clamps; coordinates
are copied versus transformed and divided by the resulting W; interchangeable
real-number algebra versus order-sensitive single-precision instructions.

Method B: execute the four complete verified shipping functions, normal entries
and Windows x64 ABI. No native-effect stubs. A establishes branch identity; B
tests actual composed writes and SSE rounding. C would be needed for real flag,
matrix/bounds/colour/UV initialization, native callers and on-screen effects;
none is claimed here. Exact executable hash and PE function extents required.

Control/feasibility: packed (16,32,64) with identity matrix gives (1,2,64,1).
Keep that first result, then discriminators: same 16 source bytes interpreted
both ways; finite packed lower/upper bounds; direct Z outside those bounds;
nonidentity transform with W=2; finite cancellation distinguishes SSE order.
Both UV branches have distinct planted values. Controlled colour components
are distinguishable. Initialise counters equal to 3; never emulate phase growth.

Budget: fresh disposable guest per case; at most 5,000 instructions and 2 seconds
per case; retain raw evidence before asserting acceptance. Stop on unknown code,
unmapped access, invalid return/ABI, identity mismatch, or failed control. Revise
the demonstrated defect rather than retrying unchanged. No exceptional-float,
overflow, unknown mode or broad domain sweep.

Acceptance: verified shipping code/constant bytes, all call edges executed, no
stubs, bounded clean return, nonvolatile registers preserved, exact finite output
and intermediate values/branch/write evidence, input/code/control state intact.
Record untouched tail bytes as observed under these fixtures, not an ABI padding
or lifetime guarantee. Retain source and checker; independent acceptance pending.

Cleanup: destroy guests; source executable read-only. No running FF12 process,
PC control, native attachment, input, save/config/reference write or fresh live
restoration receipt. Original live permission and spent S19 setup budget unchanged.
