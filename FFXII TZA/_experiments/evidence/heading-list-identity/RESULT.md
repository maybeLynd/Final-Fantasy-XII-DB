# Heading commit and effect update share a structural list path

**Answer, Method A / STATIC_ONLY.** The shipping code reads the same global
list-holder slot, `02EBEF88`, for the ordinary effect update and the
movement-linked flag commit. Both take holder `+8`, instance `+0x118`, and
node `+0x30`. The flag walk's `003A9490` is therefore structurally directed
at the effect-instance/node list that `003A8390` updates, rather than merely
using coincidentally similar offsets on an unrelated root. This is an
address-and-link proof, **not** a proof that both calls encounter the same
live instance or node.

The exact unresolved question and competing H1/H2 are in `PLAN.md`.
`check.py` reads the certified FF12 EXE (SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`),
the published function catalogue, and the two earlier heading source records.
It decodes each selected catalogue range fully, retains selected original
instruction bytes in `result.json`, and retains the previously uncaptured
`003A8390` and `0043EF40` bodies as `.bin` files. The result pins exact
driver/provider/input/body hashes. No original machine code or game ran in
this package.

| Boundary | Original-source observation | Implication |
|---|---|---|
| Existing registry control `003A8D80` | `003A8D84` loads pointer at `02EBEF88`; `003A8D8B` takes `+8`; `003A8DA4` stores current instance at `02EBEF80` | Confirms the expected effect-list root and current-instance slot independently of the two compared paths. |
| Update `003A8390` | `003A83BD` loads `02EBEF88`, `003A83C4` takes holder `+8`, `003A83D6` follows instance `+8`, `003A83DD/E7` passes instance in RCX to `0043EF40`; `003A83E0` also writes current instance to `02EBEF80` | The normal update walk uses that same global holder and instance chain. |
| Update node `0043EF40` | `003A83E7 -> 0043EF40`; `0043EF60` saves entry RCX as RDI, `0043EF9B` reads instance `+0x118`, `0043EFB0` follows node `+0x30`, `0043EFBA` calls `002F3910` with current node RCX. `002F3910` reads `byte[RCX]` at entry. | The update dispatch receives a node from that chain, under the body's early gates and normal ABI/returns. |
| Flag commit `003A9490` | `003A949A` loads `02EBEF88`, `003A94A3` takes holder `+8`, `003A94F7` follows instance `+8`, `003A94D0` reads `+0x118`, `003A94EE` follows node `+0x30`, `003A94E6/E9` passes node RCX to `0043EE70`; that dispatcher reads `byte[RCX]`. | The movement-linked store selects from the same registered structural chain and node-type byte vocabulary. |
| Temporary publication `003B3CA0` | `003B3CE0` calls `0024ED80`, `003B3CE7` calls the flag walker, then `003B3CFD` calls `0024ED80` again with the saved context in RCX. | A selected container can be published around the flag walk, then prior context republished on normal return. Identical global *address* is not stable global *content*. |

The original-code S-47 package by OPUS separately executed the shipping
`0024ED80 -> 0024FCF0 -> 003A2B20` chain in an isolated harness and observed
the published pointer write set including `02EBEF88`. That is **OPUS's prior
isolated execution**, not an ASTRA live observation or a new test counted
here. The canonical UQ-207 already established the two update drivers'
timing and common node loop; this package neither duplicates that census nor
changes its outcome. The parent heading packages already established the
four setter tails and bounded `0x67`/`0x72` readers; this result supplies the
missing structural bridge.

Canonical effect-type §2.8 already documents the construction-time copy:
`002F2D60` stores the instance's `+0x108` definition at element `+0x20`, then
copies definition `+0x44` to element byte `+0`. That is an existing source
claim, **not** a new test here. It makes another constructor sample low value.
The open discriminator is whether a selected live container and node retain
their identity and type from the movement flag call until an ordinary update,
given the `0024ED80` publication boundary and possible reuse. That would need
a prepared actual trigger, before/after pointer and type observations, and a
positive control for the observer; this static package does not supply them.

The private wrong-root and wrong-node-link instruction-byte mutations are
re-decoded by the actual checker and rejected; they never touch the EXE or a
game process. All seven selected catalogue bodies decoded to their declared
length, and the previously captured `003A9490` and `003B3CA0` body hashes
matched their immutable source records. The S-47 fixture proves behavior of
its injected state and real `0024ED80` instructions; it does not prove this
movement call's live reachability or timing.

**Boundary for consumers.** It is now supported to say the source-level flag
setter and update reader share the effect registry/list *layout and address*
under their selected call paths. Do not infer that the selected container
and a later update are the same container, that its nodes survive, that
definition type `[instance+0x108]+0x44` still equals `node[0]` in every
state, or that the update followed the setter before reuse/destruction.
`003B3CA0`'s publisher makes those runtime identity/scheduling questions
material, and they remain OPEN. Class preservation and player-visible effect
also remain OPEN. OPUS owns type/contract incorporation; independent non-author
review of this cross-path claim is required before canonical promotion.

Player version: the code for a movement-triggered effect and the code that
updates effects use the same list of effect objects. The game can switch which
list is current, so source code alone does not show that the very same effect
was triggered and then updated on screen.
