# Texture cleanup removes a key from the selected current bank

Method A STATIC_ONLY. Producer checked; independent review and canonical
consumption pending. Original EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No shipping/native/emulated/game code executed; no stubs establish
native effects. Accepted OPUS caller/release facts are reused, not recounted.

Question: what does62EC70 remove, and does this establish all-bank cancellation,
completion/drain or the texture element's wait-counter changes? The complete
204B normal wrapper selects context+56*zeroextend32(incomingR8D). It performs
two unsigned pointer-key searches in that one tree, node key+20, right+0, left+8,
root bank+18, sentinel bank+8. On a valid finite ordered unique-key tree, the
lower-bound candidate and final >= comparison admit equality only. A miss exits
before decrement, helpers and allocator. No local bank-range check or loop over
other banks exists. The retained original62BD75 caller loads context[01F7F5B8]
and bank DWORD[01F7F590] at release time, skips the call for null context, and
passes the selected element+40 key. It does not pass a captured queue-time bank.

On a hit, DEC32 bank+28 precedes16D6D0(node),16DA60(node,sentinel), then the
allocator record bank+30 slot18(record,node,28h). Only the two pre-call searches
loop in the wrapper; those calls/decrement occur at most once under normal
terminating returns. The count is the container count under distinct-allocation
premises, not an explicit write to texture element+38. Four original helper
bodies close to pointer-header loads/stores at0/8/10/18 and two call-free rotation
leaves, with no global/RIP read or async-key payload dereference/callback target.
Valid contained node/sentinel links are required. The remaining allocator slot18
is opaque; native effects, transitive callback behavior and concurrent races stay
open. Header footprints are not a malformed-pointer safety proof.

A useful discriminator needs no opaque effects: key queued in bank0, current
release bank1 empty, distinct valid banks. The original normal path returns from
the empty selected bank without any call or access to bank0. Thus the wrapper
alone does not cancel every bank unconditionally. This conditional counterexample
is a source/control-flow derivation, not proof of a naturally changed bank or a
shipping use-after-free. Whether normal bank changes occur with a pending texture,
whether drain prevents this case and who writes element+38 remain separate.

The first82B pdata entry is not the whole wrapper. It was retained once; only
122B missing normal continuations were added after matching exact parent triples.
Helper preparation first guessed two no-unwind leaves and refused before any
helper capture. Original driver/failure retained, no PASS or semantic dependency.
Actual16DA60 is867B pdata root;16D6D0 is68B leaf. Adjacent16DDD0 shares an unwind
address but is not joined to that root. Its four direct calls required only two
additional call-free leaves (92/88B). Full normal CFGs close. These are byte and
instruction coverage, not experiment totals or exception-path certification.

Reproduce with existing analysis Python and a fresh output:

    python <packet>/prove-texture-async-removal.py <fresh.json>

Four actual producer CLI refusals reuse the successful positive: consistent
changed bank stride, consistent changed key offset, missing normal tail and
failed helper-capture exit. Actual default reader/freezer qualifies nonempty
source, shared reviewed byte/access roles, normal CFG, invocation exits/output,
current drivers and result/control preimages. Required upstream failure cannot
be suppressed by a later PASS. Empty successful stderr is legitimate; missing
or empty positive stdout is not. All original driver/input/case/result receipts
remain immutable. The known native publication argument limit is checked before
copy; no publisher guard, lock, byte policy or board protection is bypassed.

Consumers: OPUS owns type/contract qualifications for selected-bank removal,
ownedBlock and distinct pendingCount; FABLE owns scheduling/cancellation/lifetime.
Do not edit their claimed consumers or treat publication as independent acceptance.
Next cheapest question is original bank-global writer/caller ordering or element
counter writer closure if unowned and still needed. Existing RNG-page correction
route remains separate; this does not silently reclassify its whole family.

Player version: cleanup targets the currently selected queue bank. If a pending
update were left in another bank, this wrapper by itself would not find it. We
have proved the conditional behavior, not that players encounter that state.

Cleanup: read-only reference/retained bytes and disposable control copies; finite
foreground scripts terminate. No PC/game/input/native/instrument/save/config/
reference or unrelated-process mutation. Parked menu allowance spent/unapproved;
EXP127 invalid. Full L1+L2 goal ACTIVE/NOT_MET; no wholeOV row closed here.
