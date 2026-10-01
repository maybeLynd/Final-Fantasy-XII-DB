# ASTRA: the voice caller can change mixer inputs

2026-09-21, **Method A**. Follow-up to the committed original mixer experiment
`6a11ec57c57dc405728b2b678abe93282706e7f1`. No new isolated execution or live game.
Consumers: the existing FABLE/OPUS pan-matrix returns and their independent review.

Player version: the voice position passed into this caller can be changed before
the mixer uses it. A script command or Sound-target read alone cannot settle the
final position. The native conditions below give a future observer precise places
to distinguish those steps.

## ASTRA — Question and sufficient method

H1: incoming front/back value is forwarded unchanged to the mixer, and spread is
unconstrained at this caller. H2: caller-side conditions override front/back and
derive/cap spread. The complete `007EDE90` body decides these structural alternatives
offline. Actual initialized objects, virtual-return values and scene reachability
still require other evidence. This is a bounded follow-through on the audio finding,
not a new runtime platform or a general audio census.

Exact reference SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base `0x120000`.
`observation.json` retains all 1,123 original bytes, hash, complete decoding, exact
anchors and the tool-resolved `1.0f` constant. `check.py` reproduces the observations
and requires exact equality. No decompiler or guessed RIP arithmetic is used.

## ASTRA — Front/back override — a concrete conditional boundary

`007EDED7` saves incoming XMM2 to XMM9. The caller initializes XMM8 to zero at
`007EDF45`. On the object-kind-4 normal-matrix path, after the three direct object
resolvers and a virtual result, it reads a **word** by this exact chain:

```text
007EE005 call 007BD8D0             ; current RSI object supplied in RCX
007EE012 mov r8,[rax]             ; vtable of returned object
007EE015 call [r8+38h]            ; RDX points at the local temporary
007EE019 mov rcx,[rax+8]
007EE01D movzx ebx,word [rcx+Ah]
007EE026 call 007CF580            ; reset temporary vtable; no payload release
007EE02B cmp bx,1
007EE02F jne 007EE035
007EE031 movaps xmm9,xmm8         ; front/back becomes 0
```

Both mixer call sites then pass XMM9 in XMM1 (`007EE0C6`, `007EE17A`). Thus the
incoming front/back value can be replaced by zero **before** `007B8430`. The exact
word's semantic identity and which real cues carry value 1 are not established here.
Do not call it a channel count, format, or spatial-mode flag merely from its offset.
This proof assumes ordinary preservation of nonvolatile XMM8/EBX across native calls;
no stub or actual virtual implementation was executed.

The earlier isolated mixer has a controlled frpan-zero result `(0.5,0.5)` for the
tested mono case. Composition suggests why this override matters, but no statement
that a particular scene takes the branch or plays centered follows from this package.

## ASTRA — Spread argument — zero or a derived finite value capped at one

`007EDF13/4E`: when the caller object's byte +50 is not 4, execution branches
straight to the normal loop at `007EE11A`, with XMM8 still zero. The special kind-4
path obtains a material header through RSI+30. For header byte +0 below `0x0F`,
DIL is zero; otherwise DIL comes from header+50 and the scalar XMM7 from header+54.
The fallback scalar is `1.0f`. Do not conflate the caller's +50 with the header's +50.

After the front/back check, DIL zero selects that same zero-spread loop. DIL one
takes this branch:

```text
007EE04E call [vtable+108h]        ; RCX = RSI object; scalar returned in XMM0
007EE05F movaps xmm8,xmm0
007EE063 mulss xmm8,xmm7          ; header scalar
007EE07E minss xmm8,xmm6          ; XMM6 loaded with original 1.0f constant
```

For finite inputs, this branch caps the product above at 1; it has no lower clamp
in this body. The normal calls store XMM8 at caller RSP+48 (`007EE0A5/159`), which
becomes **callee entry RSP+50**, the spread argument used by the isolated experiment.
The raw body also contains non-0/1 modes, special-material routing and early returns;
no claim that all modes construct the same matrix is made.

This narrows the previous experiment's open caller-range limit: the supplied spread
2 stress case is not a finite value forwarded by either analyzed normal branch of
this caller. It remains valid as a labelled isolated boundary test. Actual native
virtual-return ranges, authored scalar values, other possible callers and NaN/FP
exception behavior remain outside this result.

## ASTRA — A row is packed into an output-major matrix, then dispatched

The kernel returns one vector indexed by output for a selected source channel.
Here the source-channel count comes from `[caller+60] -> byte +4` (`007EDEEC/DF1F`),
and the loop carries it in R15D. At `007EE0EA` EBX starts at current source channel
R14D. Each output element advances EBX by R15D at `007EE0FD`, storing at local
matrix base RBP-80 (`007EE100`). The second loop repeats this indexing.

Therefore this caller's contiguous storage index is:

```text
index = source_channel + source_channel_count * output_channel
```

The conceptual source-by-output matrix from the previous package is not a claim
that this final storage is source-major. Preserve axes and physical ordering separately.
The later per-element dispatch corroborates the order: EDX = source (ESI), R8D =
output (EBX), XMM3 = the coefficient read with the same stride (`007EE263..271`).

Dispatch is another boundary: nonnull caller+68 invokes vtable+40 with the matrix
pointer (`007EE1D9..202`); other mode/flag cases may issue `00121880` per element.
Those callees' native effects are not demonstrated. A constructed matrix is not
proof that a device accepted it or that a player heard its channels.

## ASTRA — Controls, limitations and incorporation

Primary falsification checks: inspect all intervening writes to XMM8/XMM9, resolve
the min bound from bytes, compare both mixer call sites' stack/register arguments,
and corroborate the storage formula at the later per-element consumer. A nonzero
replacement source or no final argument use would refute the stated zero override;
the complete body instead shows zero creation, conditional copy and both uses.
These are static controls, not live observer controls.

`check.py` runs without emulation or FF12. No PC controls, attach, saves/configuration
or reference writes occurred; nothing needs detach/restoration. The prior B evidence
remains unchanged. Do not turn a possible branch into an observed cue or assume any
unnamed object's lifetime. FABLE should incorporate these conditions alongside the
existing mixer/spread return; OPUS should preserve exact ABI and matrix layout where
consumed. Add this to the same independent audio review, not a duplicate broad audit.

The original live request remains unresolved only for an actual scene/device claim.
Its observation must follow target -> caller override -> mixer input -> constructed
matrix -> dispatch -> accepted device effect, with the relevant stages established
individually. Live authorization remains active; this package did not need it.
