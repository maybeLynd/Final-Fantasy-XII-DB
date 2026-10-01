# Texture bank submission is distinct from key execution

Method A STATIC_ONLY; producer checked, independent review/canonical consumption
pending. Original EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. Six exact byte ranges close three normal CFGs and a 15-byte tail
callback; no native/emulated/game code executed and no stub establishes effects.

185A50 passes its pre-call DWORD bank[1F7F590] zero-extended in R8D, callback
186610 in RDX and incoming RCX to5FEA50. After normal return it rereads the
global bank, INC32/AND3/stores it and returns the new bank in EAX. It overwrites
submission status without testing it. Under unchanged/no-interference calls,
four invocations rotate all four residues; those invocations are not frames.

5FEA50 saves callback/data, rejects NULL callback with1, otherwise calls600B30
with EDX0/R8D1 and conditionally context vslot10 if AL0. These are opaque
boundaries. Afterward it attempts a128B cursor reservation, wrapping to begin
when needed under unsigned bounds. A nonNULL reservation sets batch begin if
unset/end and writes DWORD opcode2F at0, QWORD callback at8 and data at10,
then returns0. Failed reservation returns0D without payload writes. This body
contains no direct call of the saved callback, but opaque callees are not a
transitive no-callback proof. A conditional post-opaque empty-buffer state
produces0D while185A50 still advances; not a natural allocation-failure witness.

186610 reads DWORD[input+10], loads the CURRENT context[1F7F5B8] and tails
62EBC0. The stored shape is compatible with passing the command's address,
but the actual opcode2F interpreter and that callback ABI remain OPEN. A record
written is not a command executed. The context is not saved in this command.

62EBC0 selects one bank at context+56*zeroextend32(EDX), starts at bank+10 and
ends at sentinel bank+8. It calls key[node+20] virtual slot0 BEFORE16D6D0
computes the live tree successor. This is different from1F7F598/186230's pair
queue with a captured end. On normal completion it rereads root bank+18, calls
220390 for a subtree and allocator record bank+30 slot18(record,node,28h),
then resets the links/root/color/count28. Callback/tree mutation, subtree and
allocator effects remain opaque. Container count28 is not texture element38,
nor GPU completion. Finite valid stable tree/buffer/ABI premises are explicit.

Raw capture uses the shared reviewed role adapter and actual byte re-decoding.
Complete normal fragments are matched through exact parent triples, not shared
unwind addresses. The candidate retool view supplied positive address discovery
only: no all-writer/caller, indirect-reference or negative-coverage claim.
Reproduce the local proof with existing analysis Python and fresh output:

    python <packet>/prove-texture-async-bank-dispatch.py <fresh.json>

Four actual CLI refusals reuse the positive: consistently changed opcode,
consistently moved data offset, missing normal consumer tail and failed capture
exit. Failed upstream invocation cannot become semantic PASS. The default
freezer also checks actual producer/control exits, nonempty positive output,
current driver/result/raw identities and concrete refusal results. Driver,
input, case, result and invocation receipts remain immutable. Producer controls
are not independent review, and publication is not canonical acceptance.

OPUS owns the128B record/callback/return ABI and distinct counters. FABLE owns
bank submission versus execution, traversal and lifetime/scheduling premises.
Next discriminator: original opcode2F interpreter branch, callback argument and
command stepping; then natural initialized caller/scheduling if still needed.
Actual initialized bank/context, reachability, timing/thread, native success,
natural pending work in another bank, counter38 writers and lifetime stay OPEN.

Player version: the game writes a request and moves to the next work bank. A
failed request still moves the bank. We know how the bank-processing routine
handles keys; we have not yet proved which interpreter executes that request.

Cleanup: only read-only shipping/retained files and disposable control copies;
finite foreground scripts terminate. No PC/game/input/native/instrument/save/
config/reference or unrelated-process mutation. Parked menu spent/unapproved;
EXP127 invalid. Full L1+L2 goal ACTIVE/NOT_MET; no wholeOV row closed here.
