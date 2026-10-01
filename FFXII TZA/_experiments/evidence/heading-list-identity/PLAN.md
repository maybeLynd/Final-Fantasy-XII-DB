# Heading commit / effect-update list identity

Question: do the movement-linked `003A9490 -> 0043EE70` flag setters and
the `003A8390 -> 0043EF40 -> 002F3910` update readers walk the same
*registered list topology*, or merely two lookalike node shapes? This is the
remaining static prerequisite before asking whether one live node is both
set and consumed. OPUS's existing UQ-207 already answers the two update
drivers' timing and per-node loop; do not repeat that work.

Hypotheses: H1 both load the exact singleton `02EBEF88`, traverse its `+8`
instances, then the instance's `+0x118` nodes linked at `+0x30`. H2 one uses
a different root, offset or receiver. H1 would support a shared structural
path but would **not** prove the same node survives between calls, that a
caller invokes both, or which frame schedules them. In particular, the
`003B3CA0 -> 0024ED80` context publication can replace the value in the
same global slot; compare its original call/restoration boundary and consume
the already-published S-47 original-code test, rather than assuming a stable
population merely because the address matches.

Method A: read only verified shipping EXE instructions for the bounded
`003A8390`, `003A9490`, `0043EF40` and `0043EE70` bodies, plus the
`003B3CA0` publication boundary, with `003A8D80`
as the already-documented registry control. Validate full decoded sizes,
RIP targets, immediate calls and the register assignments at each boundary.
Consume the published `002F3910` type-method table and UQ-207 for the
downstream handler, rather than recapturing them. Positive control is the
known `003A8D80` root `02EBEF88`; same-count wrong-root and wrong-link
in-memory mutations must be rejected by the checker. Stop at structural
identity; actual initialized ownership/reuse or scheduling requires a
separate live-only question with prepared state.

Source identity: certified EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
No game, native execution, save/config/reference write or menu setup.
