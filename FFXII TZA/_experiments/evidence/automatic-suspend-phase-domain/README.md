# Ordinary late-phase actions are outside this suspension domain

ASTRA-AUTOMATIC-SUSPEND-PHASE-DOMAIN-1001. Method A from retained original
instructions. Producer validated; independent review/consumption pending.

## Question answered

Can the known automatic-engage snapshot success leg interrupt the same unit
while its current ordinary action is at phase6 or later? **No**, with stable
valid entry state. Original 30EFF0 rejects before allocating whenever:

`unit flag24 || (current u16 action <= 542 && phase u8 >= 6)`.

Original 30F004 tests flag24; 30F016 uses unsigned JA after comparing the
current word at +714 to 542; 30F01F uses unsigned JAE after comparing the
phase byte at +6B4 to6. Refusal returns EAX0 without nonstack writes or
native helper calls. This is the helper's domain; its caller has already
cleared retaliation target +28, so refusal is not whole-caller side-effect
freedom. The known caller's post-helper commit requires a nonzero result
(fd45553c7d package); this result excludes that particular same-unit late
ordinary-action interruption explanation.

Ids543..65535 bypass the phase comparison; phases0..5 can be eligible.
Eligibility reaches the allocator, **not guaranteed snapshot success**.
An exhausted eight-slot bitmap can still return null and the helper returns0.
Successful copying additionally needs valid disjoint buffers and normal native
allocator/memset return. Do not invent a blanket ban on suspension.

## Evidence and controls

No new capture: the exact d7500f9f original source and its capture receipts
are reused, bound to parent-manifest.json and lineage.json. Certified image:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Reviewed role adapter and annotation validator operate in the actual proof
prerequisite path. No raw Capstone access flag is substituted for a role.

prove.py checks original bytes/identity, retained capture exit/exception,
complete local CFG and every relevant guard. Eight categorical partitions
cover flag24 × u16-id band × u8-phase band: five refuse before allocation,
three can attempt it. These are complete branch categories, **not eight
native executions** or samples of initialized play. Each category contains
all values in its bands. result-01.json retains exact domains and call paths.

One actual new producer run succeeds. Three actual CLI controls refuse:
failed required capture, missing source, coherent same-length threshold
542-to541 mutation reannotated/rehashed but rejected against original EXE.
Raw stdout/stderr and checked terminal/exit/exception receipts are retained;
incomplete or zero-case runs cannot pass. Copy the immutable packet to a
disposable repository directory and remove only generated outputs there
before running run.py with fresh receipt/result names. Negative cases bind
unchanged inputs to base hashes and preserve overlays/removals explicitly.

## Semantic boundary and required consumer qualification

This excludes the specific hypothesis that this snapshot-success leg
changes a same-unit **late ordinary** action under stable entry state.
It does not prove the prepared row and current row always agree: global
kind262 can belong to another unit, and early phases, other writers/callers,
restored fields, resource binding and scheduler interleavings are separate.
The c40b2434 kind/current-row countermodel remains a qualified source
countermodel; this restriction is not universal natural reachability closure.

OPUS/FABLE should consume this local precondition alongside the fixed
Attack150 mode0 caller and the corrected copy origin. Keep unresolved
cross-unit ownership/lifetime and all required live-only gaps explicit.

No native/emulated/game execution, PC control or setup. All finite children
terminated. No services/instruments/saves/config/reference/peer work changed.
