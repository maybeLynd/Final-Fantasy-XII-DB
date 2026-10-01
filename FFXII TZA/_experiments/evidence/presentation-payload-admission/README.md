# Presentation payload admission and resource boundaries

ASTRA, 2026-09-12. Findings are in
[render evidence sections 9–11](../../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md#9-payload-defaults-and-resource-admission--original-instructions).

Claim: determine which defaults and resource reads establish the payload required
by the recovered 64-slot container, and what its cleanup actually changes. Existing
container work stopped at `0041CB90`, `0041D220` and `00372280`. Distinguishing
observations are exact store extents, operation order before a failed admission,
native cleanup writes and the pointer arithmetic used by its resource dependencies.

Method **A** is sufficient for these bounded instruction-level claims. The four
body receipts contain 19 complete newly read shipping bodies; two prior bodies
(`0041CA70`, `0041CF00`) are reused from
[the previous effects receipt](../presentation-entry-lifetime/effects.json).
All collectors check reference EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, preferred base
`0x120000`, instruction extents and Capstone 5.0.7 decoding. The function-index
identity is retained. [review.json](review.json) records byte-contiguity/hash checks
and actual final RET/JMP boundaries. An initial review assertion wrongly required
RET and rejected the legitimate `00409F50` tail wrapper; that correction is recorded.

The opposite branches are read explicitly: null entry / offset -1 versus a
nonnull entry whose base getter returns zero; absent versus admitted `+368`;
cleanup flag clear versus set; selected bone index versus FFFF. The cleanup's
complete outgoing graph contains only two pure compressed-pointer decodes. These
are static control-flow comparisons, not executed negative controls. No new B
execution, live observation, reconstructed fixture or mutation campaign is claimed.

The results narrow the database in three ways:

- Base reset preserves unlisted bytes and most of `+2E8`; admission can return
  zero after fields and linked model resources have changed. A valid primary
  resource pointer alone does not guarantee the later model-group accesses.
- Cleanup `00372280` clears selected bone flags and two vectors, with no allocator
  or release callback. Native group refresh also writes linked bone pointers.
- Section resolution can narrow and sign-extend a full pointer; child-container
  addressing instead zero-extends in its container branches. One child path reads
  the offset table before checking the final index. These are distinct contracts.

The 1.0 and 30.0 values in [constants.json](constants.json) are the image's initial
bytes, not captured live settings. The actual `003E1C50` and `0040ED90` effects,
source ownership, cleanup-flag writers, external ID invalidation and native timing
remain open. No omitted callback is replaced by a stub and then credited with its
native effects. Semantic/type propagation requires peer agreement.

The five `collect-*.py` files reproduce their receipts into the existing ASTRA
work directory with the existing analysis Python environment. They read the
reference image without modifying it. The manifest seals this package; prior
experiment and mutation histories remain unchanged.

Receipt serialization: the first publication preflight refused the collected JSON
hashes because Git normalized their CRLF line endings. No commit followed that
failure. Canonical receipts now use LF; the manifest retains every original raw
receipt hash and the verified reversible LF-to-CRLF transform. Instruction bytes,
body hashes and parsed receipt data are unchanged; original work receipts are untouched.
