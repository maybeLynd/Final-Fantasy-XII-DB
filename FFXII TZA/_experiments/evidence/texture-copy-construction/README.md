# Texture element construction: copied counter, initialized tail, capacity precondition

Method A STATIC_ONLY, producer checked and independent acceptance pending.
Question: does the original61D100 helper clamp/reset existing elements, or copy
the requested prefix and initialize a separate tail? This matters for ABI,
buffer bounds, async data and wait-counter lifetime. Shipping EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000; complete121-byte unwind root plus133/93-byte no-unwind leaves with
branch closure and original padding, actual shared reviewed role adapter and
decoded-byte prerequisite. No FF12/native/emulated function was executed.

Established locally: EDX low32 is new countN, R9D low32 is copy countK, R8 is
the source pointer. N=0 returnsNULL with no copy/init, N=1 chooses helper-record
RCX+8, N>1 calls17D260 for88*N bytes/alignment8. NULL output skips both leaves.
With valid nonNULL storage the caller copiesK, then initializesu32(N-K) at
output+88*K. It has no local clamp or drain. For ordinaryN-record output,
K<=N is a required capacity precondition. K>N is not sanitized: N2/K3 would
already copy a third record beyond176-byte capacity and requestFFFFFFFF tail
records. This is a conditional source arithmetic witness, not an observed
shrink bug, a native run, or proof a shipped caller violates the precondition.

The copied prefix preserves DWORD counter+38, texture/index asyncdata+48/+50,
and the previously accepted data fields; +40 is assignedD54348. It does not
locally drain/reset those counters or rebind copied userdata to a new owner.
The fresh tail zeros QWORD0..30 and DWORD38 and binds40, but leaves48/50 and
padding3C/54 untouched locally. A successful allocator/base constructor may
have other effects; neither is certified by this source. 'Initialized record'
must not silently mean every member was zeroed.

The accepted OPUS513baa66d texture T2 stride/field layout is reused, not rerun
or credited as a new census. New claims are the composed61D100 count/ABI/order,
prefix counter preservation versus tail zero, untouched userdata and capacity
condition. Full native counter writers and natural initialized values remain
OPEN. The reference preparations are candidates only: controls find the two
known623DF0 drain calls and621FF0 table slot; copy caller61D14C is validated by
the new full code source. Absence of more raw patterns never proves no indirect
or computed callers/writers. Raw preparation01 and its original driver preimage
remain distinct from the parameterized02 driver/result.

Reproduce with existing analysis Python and a fresh result:

    python <packet>/prove-texture-copy-construction.py <fresh.json>

Four actual CLI controls reuse the completed positive and refuse missing
wrapper, falseK/N annotation, byte/annotation-consistent changed source-count
register and wrong initializer extent. These are synthetic producer controls,
not game experiments or independent acceptance. Original code/data/reference
results and driver identities are immutable; byte-preserving policy precedes
manifest. Allocation success, storage/stack/nonwrapping and normal ABI-return
premises are explicit. General overlap, alias, old-storage disposal, rebinding,
queue removal, natural shrink/caller reachability and lifetime remain open.

OPUS owns exact ABI/type/contract incorporation; FABLE owns scheduling/lifetime
implications. Only new claims need independent review, not the already accepted
stride/layout. Next cheapest discriminator is61D100's original calling context:
does it guaranteeK<=N and appropriate disposal/drain? Prove that guard/order
before any runtime counter probe. The earlier generic widget protocol already
states message18-before-storage-retention; no unchanged widget recapture was
performed. Natural title pending/deferred applicability still remainsOV29.

Cleanup: bounded original file reads/static analysis only, all known scripts
terminal. No PC/game/input/instrument/save/config/reference or peer-process
writes; EXP127 invalid and parked menu spent/unapproved unchanged. This packet
does not close wholeOV29 or the L1+L2 goal. Manifest integrity, producer controls,
independent acceptance and canonical consumption remain distinct.
