# Presentation entry initialization and lifetime

ASTRA, 2026-09-12. Canonical findings are in
[render selection evidence §6–8](../../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md#6-the-render-root-constructs-64-reference-slots).

Claim/hypotheses: the concrete constructor and ID lifecycle must establish the
preconditions absent from `0051F240`. Existing lookup execution proves cache writes,
low-half indexing and null-base boundaries, but not native construction or ownership.
Distinguishing observations are reset/storage order, literal capacity, ID production
and validation, node release writes, and which rebases ignore the lookup refresh bit.

Method **A** is sufficient for this bounded package. Five complete-body collections
contain 22 verified contiguous shipping bodies from EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, preferred base `0x120000`.
They preserve instruction bytes, extents, hashes, Capstone 5.0.7 and function-index
identity. `review.json` records the exact body inventory and byte-contiguity/hash
checks. Known constructor/admission/unlink branches are positive controls; the
direct-call graph led to the full root constructor rather than a no-caller claim.
`0051B870` was an adjacent discovery candidate, read but not used as lifetime proof.

There is **no new execution or mutation campaign**. The previous package's original
lookup cases remain at their original scope. Source/offset, template-copy and callback
effects here follow exact code, not a reconstructed implementation agreeing with its
own fixture. Body/identity disagreement or an unread callee needed for a stronger
claim leaves that claim open instead of being replaced by a stub.

Limits: `0041D220` resource admission, `0041CB90` defaults, resource helper results,
`00372280` cleanup, external ID ownership and integrated scheduling are not established.
The root's local reset-before-storage sequence is proved statically, not observed as
live initialization. The generic interface can have other callers and malformed state.
No live-game controls resumed after the exit-and-cleanup authorization.

The five `collect-*.py` files reproduce the body receipts into the existing ASTRA
work directory using the existing analysis Python environment. `manifest.json` seals
all package files except itself; the reference binary is read only. Prior evidence
and mutation histories are preserved.
