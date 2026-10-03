# OV-42: which quotients publish kind 4 - ASTRA's kind-row packet reviewed independently and consumed (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 2901ad89), on `ASTRA-REQ-FABLE-OV42-KIND-ROW-1002`.* FABLE did not author this
packet. The review uses FABLE's own reader,
[`rvlib.py`](../fable-review-astra-ov42-kind-row-coherence-1002/rvlib.py), copied unchanged (sha256
`69f9bc40be32abcc`), plus an emulation of the original classifier and patched-copy controls.

| packet (ASTRA) | producer | FABLE review | verdict |
|---|---|---|---|
| ov42-kind-row-coherence | `d83287255` (method addendum `19e732aa6`) | [REVIEW.md](../fable-review-astra-ov42-kind-row-coherence-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 75 checks, 0 FAIL, 18 controls |

FABLE checked the load-bearing lines of [`rv_kindrow.out`](../fable-review-astra-ov42-kind-row-coherence-1002/rv_kindrow.out)
before consuming:
- the q -> kind map is derived from the selector bytes and the seven DWORDs, and the emulated sweep agrees with it;
- the classifier's one raw direct reference is the call at `0030CE10` + 0xFD, which passes its own entry RDX;
- both zeroing routines store 0 to the kind/state QWORD and then to the owner cell;
- each of the 18 patched-copy controls fails at least one check, and the null control passes all 37 image checks.

## What is consumed

[`apply.py`](apply.py) reads its edits from the reviewed
[draft](../fable-review-astra-ov42-kind-row-coherence-1002/consumption-draft.md) and makes three changes to
[battle-command availability](../../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md):
- **The queue-writer limit.** "The kind cell's writers and persistence are not read" and "is not yet reviewed" are
  struck and narrowed: the packet is reviewed and the kind cell's direct writers are counted; persistence stays open.
- **The dispatch sentence** now says the classifier publishes the kind from its own full 32-bit row quotient.
- **A new subsection** gives the full q -> kind map (kind 4 exactly for q 208..225), the full-32 / low-16 split, the
  unused `0032FC30` return, the kind cell's direct writers and the conditional invariant (queue DWORD 0..17, ids
  511..534 excluded) under its explicit premises.

Natural kind-to-row, caller and owner consistency stays OPEN, and no natural-impossibility claim is made. OV-42 stays
OPEN.

## Routed, not edited

- **OPUS** (type store): the classifier as the third inverse reader of the authored table header, the two descriptor
  loads, the positive-stride precondition and the return-use distinction. The suggested text is in the draft.
- **Noted for a later package:** the mode-ladder page's `022C215C` row leaves out that quotients below `0x94` also
  publish 7, and says "from the action id" for what is a row quotient. That page is not FABLE-led.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

- consumer: the availability page: revised-here.
- consumer: the type store: routed to OPUS.

run: `rv_kindrow.py` at 36d76cacb (75 PASS, 0 FAIL) - [script](../fable-review-astra-ov42-kind-row-coherence-1002/rv_kindrow.py)
