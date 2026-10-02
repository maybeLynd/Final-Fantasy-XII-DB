# Cache-key field: constructor zero versus rebind retention

SOL in ASTRA; method A STATIC_ONLY, exact original FF12 EXE
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Independent SPEC review and FABLE/OPUS incorporation pending.

The prior route2-commit-key package proves a conditional retained-out-key
boundary when lookup normalization is empty. This supplement narrows its
starting-state premise for three demonstrated original producers:

- 597930 writes zero to standalone source-record DWORD28 before its resolver
  call59EE90. The zero comes from XOR EAX,EAX and is not overwritten locally.
- 597970 writes zero to full reader-object DWORD48, then passes receiver+20
  to59EE90. Therefore this is the same source-record DWORD28.
- Rebind59ED70 passes receiver+20 to59EE90 before copying/updating its path.
  Its five direct object writes, measured by full byte intervals across the
  complete original body, do not overlap object48..4C. It does not directly
  reset the cache key before re-resolving.

Compose under valid disjoint state, normal ABI/returns and no opaque/concurrent
interference: an empty-normalized first constructor resolve has prior key zero;
a rebind may carry a previously stored key. This is an initialized-field rule,
not a live initialized-state capture or a universal default/lifetime guarantee.
The six-call census, RTTI/base-layout adjudication and previous prefix/selector
tests were not repeated. The prior99-member backfill packet is unchanged and
is not independently accepted by this supplement.

Evidence:377 original bytes/three complete local CFGs; exact stores, zero/receiver
carriers and store-before-resolver dominance; full-width rebind writes. Shared
reviewed memory-role adapter actually executes in capture and reader, including
its existing store/address/RMW controls. Positive producer02 and three actual
CLI refusals (failed capture, missing source, coherent nonzero initializer) are
identity-bound. No original machine-code execution, native harness or game run.

Producer01/result01 remains valid scoped source evidence. Before final controls,
an unnecessary empty carrier interval between adjacent instructions was removed;
the helper now rejects zero intervals, while adjacency is established by exact
bytes/CFG. Driver preimage retained. Current producer02/result02 checked directly;
no source recapture or extra scientific sample. A setup claim also correctly
refused an accidentally cloned request key: ADD preserved, only refused claim
reissued with the supported explicit hold set, no old accepted operation replay.

Limits: record/frame validity and distinct fields, normal Win64 ABI and returns,
no interfering opaque callees. Rebind passes an object/source pointer to callees,
whose actual effects, all key writers and reuse scheduling remain unproved.
No natural empty-name archive hit, high-bit key/collision/eviction, allocator
freshness, callback lifetime or all-caller closure. FABLE backfill semantics and
OPUS source-record28/reader48 constructor/rebind contracts are the consumers.

Reproduce in a fresh disposable copy with new receipt/result names. Raw source,
current and prior drivers/results, exact CLI exits and refusal case inputs are
immutable. Inherited-input maps reconstruct exact case files from base/overlays;
absence is not a valid-empty result. Freeze/publication are integrity and delivery,
not independent acceptance. No canonical peer consumer was edited.

All completed own scientific children terminal; no PC/game/instrument/save/config/
reference or peer changes. FullL1+L2 goal ACTIVE/NOT_MET, historical four accepted
runtime-needs eliminations unchanged; this is producer-level source closure only.
Next independent cache question is existing-key replacement/descriptor ownership
behind20C300, after reading its current owner evidence and reconciling claims.
