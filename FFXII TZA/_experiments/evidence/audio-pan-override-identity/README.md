# ASTRA: a native consumer of the SAB/MAB header's +0x0A word

2026-09-21. **Method A**, no original-code execution or live game in this package.
Follow-up to original mixer `6a11ec57c` and caller boundary `625bd0a75`.

Player version: on the verified in-memory-bank path, a word in the sound-bank file
can make the voice routine replace its front/back value with zero. We have identified
a use for a field the database previously called unread. We have not established
which running scenes take this branch or what all other field values mean.

## Question and competing identities

The caller `007EDE90` reads a returned wrapper's +8 payload, then compares payload
word +0A with 1. H1: that is an authored bank-header word. H2: an unrelated runtime
descriptor field. A numeric displacement is insufficient to choose. Reuse the known
handle/accessor routes, verify the vtables with original RTTI, and follow initialization
to the actual file pointer. This needs no new live experiment.

Exact executable SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base `0x120000`.
`check.py` verifies eleven complete original bodies, decoder coverage, critical anchors,
RTTI locator self-identity, class names, slot targets, magic constants and the already
retained full caller body. `observation.json` preserves raw bytes and all identities.
The existing RTTI tables were used as locators, then checked against original data.

## The verified pointer chain

1. `007BD8D0` reads owner+20, wraps that handle in a stack temporary and calls
   `007B2470`. The latter checks the low tag byte equals 1, searches its registry,
   checks occupancy and exact handle equality at the returned object's +10.
   It is a resolver; its name alone does not prove the resolved object's class.
2. For an object whose primary vtable is **OnMemoryBank `01CB83F8`**, slot 7 is
   **`007E2A70`**. Original RTTI names `.?AVOnMemoryBank@Driver@Sd@SQEX@@`; the
   locator has zero subobject offset and a matching self RVA. The constructor
   `007E29C0` installs this primary vtable and clears its +50 pointer.
3. `007E2A70` loads object+50 into RDX, calls `007CF540` with the caller-provided
   temporary as RCX, then returns that temporary. `007CF540` installs vtable
   `01CB6E30`, whose original RTTI is **AudioBinaryFile**, and stores the supplied
   payload pointer at wrapper+8. Thus `007EE019` obtains **bank+50's payload**, not
   a wrapper field mislabeled as file data.
4. The named initializer `007E2AD0` reads its descriptor type at +18. Type 1 checks
   descriptor+20 via `007CFF90` against original **`sabf`**; type 2 checks it via
   `007D07A0` against **`mabf`**. On successful magic check, `007E2B41/4B` stores that
   exact descriptor+20 file pointer at bank+50. The error string independently names
   `OnMemoryBank::Initialize`. The following base initializer `007D09B0` is also read
   in full: it writes +10/+40/+20/+18/+48 and returns zero, preserving +50. Its +10
   store uses descriptor+0, consistent with the resolver's handle-equality check.
5. Therefore, on this validated class/binding path, the caller's `word [payload+0A]`
   is **file-header +0x0A**, the `_param` word on the SAB/MAB format page. If it equals
   1, `007EE031` replaces XMM9 (incoming front/back value) with zero before the normal
   mixer call sites. This is an identified conditional consumer, not a universal
   rename or description of all header values.

The secondary Bank vtable is not interchangeable with its primary vtable. The
current instance must satisfy the known primary-object identity for this composition.
No live resolver/slot read or default lifetime assumption is smuggled into this chain.

## Streaming branch and wrapper lifetime limits

The original primary StreamingBank vtable **`01CB84E8`**, independently checked by
RTTI, points slot 7 at **`007E2E80`**. That getter wraps **bank+88** with the same
`007CF540` helper. This establishes its accessor/payload structure only. We have not
followed its initializer/backing-buffer contents, so the in-memory file-binding proof
must not silently be extended to every streamed instance.

The earlier caller package labelled `007CF580` “release local temporary.” Reading
its complete **11-byte** body narrows that wording: it installs the AudioBinaryFile
vtable at temporary+0 and returns. **No pointer payload is freed or cleared there.**
This is a temporary wrapper's vtable reset/destructor boundary, not evidence for a
bank/file ownership release. The prior caller raw code and matrix result are unchanged.

## Established, refuted and open

- **Established:** class-qualified wrapper identity, bank payload field, magic-checked
  source-file binding for OnMemoryBank, and a native conditional read of header +0A.
- **Refuted as a present global conclusion:** treating header +0A as having no known
  reader after this result. The page's old “no reader in the functions read” was a
  correctly scoped historical statement; preserve its provenance rather than claim
  the prior scan failed.
- **Still open:** why the field takes its full range of values, which relevant shipped
  banks have value 1, actual scene/cue binding, real virtual targets, streaming-buffer
  initialization, other registry object classes and audible output.

The format page reports 350 distinct SAB values and `0x2710` for its observed MAB
population. Those are **existing corpus observations**, not rerun or enlarged here.
Do not classify all non-1 values as inert; only this caller's equality test is settled.
The isolated frpan-zero mixer control can explain the local mathematical consequence,
but an actual voice or device result still requires its own evidence.

## Controls and consumers

Positive identity controls are the two distinct primary bank class names and slot-7
targets, the wrapper's independently named AudioBinaryFile RTTI, and separate SAB/MAB
magic checks. The OnMemoryBank constructor, getter and initializer converge on +50;
the streaming getter's different +88 is preserved as a boundary, not forced to match.
An unrelated wrapper type, different payload offset or initializer rebase would refute
the claimed file-relative access; original bytes show none on the verified path.

FABLE owns SAB/MAB format and audio semantics; OPUS owns corresponding field/contracts.
They should record the first known consumer and its exact condition, keeping overall
field meaning open. Include this chain in the existing audio-matrix review instead of
requesting a new broad audit. Independent review and canonical incorporation are pending.

No PC controls or @runtime reservation were needed. No game process, save, config or
reference state was modified. This static evidence needs no attach/detach/restoration.
Run `check.py` from the project venv for read-only identity reproduction.
