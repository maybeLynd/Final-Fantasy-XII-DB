# Original skeleton reference producer and workspace binding

## Question answered

What stores the render element's `+94` skeleton reference, and can its producer
be described without another live skeletal-reset trace?

Method A verifies four positive shipping-code stores already listed in the
current access table: `00371435`, `00371469`, `00372914`, `003729A9`. The type
row still contains its older no-writer-found census note. Preserve that history
and add the current producer explanation; this is not an exhaustive writer
census or a claim that the canonical access index regressed.

## Original binding flow

`00372820` stores `Encode(caller argument 5)` into element `+80`. It initializes
`+94` to encoded NULL and `+90` to zero. If caller argument 7 supplies a non-NULL
source blob, it resolves the workspace representation through `003AB7F0`,
stores the encoded resolved workspace in `+84`, and puts its computed offset in
`+90`. It then derives `+94` from that workspace and offset.

The original call at `003729BD` receives decoded `+94` in RCX as destination,
argument 7 in RDX as source, and the sign-extended DWORD of argument 8 in R8 as
length. The original three pushes plus `SUB RSP,0x30` make a 72-byte frame:
argument 5 entry `+28` is read at current `+70`, argument 7 entry `+38` at `+80`,
and argument 8 entry `+40` at `+88`. Its upper 32 length bits are not read.
Negative lengths are not asserted safe. This establishes call arguments, not
effects of a substituted copy stub or a real execution of the copy routine.

The offset calculation uses original DWORD resource-header `+C` times `0x149`,
adds zero-extended WORD `+38`, forms `2*x+15` in EAX, then applies the original
CDQ/AND-15 correction and mask `FFFFFFF0`. Signedness and 32-bit wrap remain
part of that operation. No unrestricted safe-size or authored-domain bound is
claimed.

`003713C0`, also called afterward by the binder, refreshes the workspace from
element `+80` into `+84`. Group WORD `+16 == FFFF` returns before clearing `+94`.
Otherwise it writes encoded NULL first. Only a non-NULL decoded `+A0` plus
signed-positive `+90` admits a new `+94`; a non-NULL decoded result then admits
`003E1C50`. Section lookup and that initializer's native effects remain outside
this slice.

The target reference is a location in caller-supplied resolved workspace on
this path. Optional caller bytes are copied there through the original call.
The workspace allocation/ownership, source blob's authored or runtime origin,
internal skeleton arrays and later users' lifetime remain separate questions.
Neither pointer arithmetic nor copied bytes establishes those facts alone.

## Exact-width reference arithmetic

The decoder zero-extends ECX and adds the full 64-bit arena base. The pointer
addition at `00371459` / `00372991` is in EAX, so it truncates to 32 bits.
MOVSXD makes a signed 64-bit temporary, but the encoder reads ECX and subtracts
only the base's low DWORD. Under a stable base:

`newRef = low32(ref84 + offset90)`.

The sign extension does not survive into the stored reference or final decoder.
For example at base zero, `CB000000 + 6000` stores `CB006000` and decodes to the
low positive address `00000000CB006000`, despite the intermediate signed
temporary. This is source arithmetic, not a captured process address. General
equality follows the original modular operations; the three retained examples
are mathematical controls, not native runs. Changing the base between calls or
passing an arbitrary high-address caller workspace is outside the proof.

## Evidence, controls and repaired producer

Reference EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
New source contains the two complete producer bodies and ten-byte decoder.
The encoder and pointer reader are retained with their original capture
receipts/manifest from `134687c7d25bd0f1a4e46ae98d4088532e55537c`; no recapture
or execution is credited for them.

The actual capture uses the shared reviewed access-role adapter. The producer
checks both captures, exact original bytes, complete local CFG, positive writer
width/roles, correspondence to the retained access table, instruction/dataflow
assertions, nonvolatile carriers and dominance before the optional copy.
Normal ABI, valid private frame/row/table, nonaliasing, native normal returns,
stable base and no interference are explicit premises.

`proof-01` is INVALID_PRODUCER_ORDER. A retained-source metadata gate had been
placed after output writing. It passed on the actual input, and earlier byte
and manifest gates also passed, but the unsafe procedure was discovered before
publication or consumer delivery. The exact old driver/result/receipt and
additive disposition are preserved. The gate now precedes semantic processing.
The focused source-order regression rejects the actual old producer and accepts
the repaired one. `proof-02.*` / `result-02.json` are current.

Three actual CLI refusal controls cover failed capture, missing source and a
coherent skeleton-reference store-offset mutation. The concrete source-order
control is separately labelled static. All raw input/case/output identities
remain available. No failed/incomplete result is PASS. An initial patch with a
placeholder context was refused without a source change or test execution.

Use the existing project Python with `run.py proof-new prove.py result-new.json`.
Outputs are immutable. Producer validity, manifest integrity, independent
acceptance and canonical incorporation remain distinct.

## Consumption and remaining work

OPUS should add the positive producer/width/ABI interpretation after independent
agreement, keeping the old census note historical. FABLE should distinguish
the encoded binding, caller workspace, optional copied content and internal
array storage instead of inferring storage kind from a zero arena base.

Caller argument 5 allocation/extent/ownership, argument 7 source and argument 8
domain, internal skeleton `+78`/`+88` arrays, scheduling and normal reset entry
remain open. Four positive supplied sites do not prove an all-writer/lifetime
closure. EXP127 remains INVALID_POST_TRACE; its completed failure-aware review
does not convert it into a healthy live experiment. The already accepted
zero-base/low-address correction is reused, not retested.

No game, PC control, native harness, instruments, saves, settings, reference
bytes or peer processes/files were changed. All our children are terminal.
The full L1+L2 goal remains ACTIVE. Parked menu allowance remains spent and its
extension unapproved; unrelated evidence work continues while review waits.
