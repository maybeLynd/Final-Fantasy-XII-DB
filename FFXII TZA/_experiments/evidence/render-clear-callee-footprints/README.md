# Original render-clear composed write footprints

**STATIC_ONLY, method A. Producer evidence; independent acceptance and canonical
consumption pending. No FF12 instructions executed or live game used.**

Question: can the exact helper calls and direct stores in `0041F730` replace the
parent slot proof's blanket opaque-helper preservation premise for slot ID0 and
active284? H1 leaves writes to either field possible through the opaque helpers.
H2 bounds each supplied helper through the actual caller receiver/index domain.
Original code distinguishes these hypotheses without a game session.

For the player: FF12 resets a character-rendering slot before using it again.
This package checks what the reset writes, especially the empty-slot marker and
active flag. It does not establish every caller's lifetime or scheduling.

## Inputs and provenance

Shipping EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base120000h.
New capture contains five complete local bodies totaling124 bytes:
6C0520..6C053A,46D110..46D11C,202C70..202C8F,3E5D00..3E5D2C,3E37E0..3E37EB.
Exact reader/driver/tool/interpreter and raw stdout/stderr hashes are in the
capture/status/result/manifest receipts.

Caller41F730..41FBE8 comes from the immutable frozen parent slot packet,
manifest `a2bcea12693de55748686a2cef48402c0189666974a8af9a8c0720b2717c73ee`.
`lineage.json` preserves **frozen/publication-ready at read**, not publication or
independent acceptance. Subsequent parent publication does not change that
history. The original four parent ranges are retained and byte-checked, but
only the required clear-caller CFG is used for this proposition. No recapture.

`prove.py` checks both actual capture receipts, wrapper completion, retained
manifest members, reviewed adapter annotations, current EXE/raw bytes, complete
local CFGs, exact operations, dominance, register carriers and all write spans
before emitting its immutable result. Capstone register-access metadata is
used only for register carriers; memory roles use the shared reviewed adapter.

## Established result

| Supplied call | Exact caller target / footprint | Meaning and limits |
|---|---|---|
|6C0520 at41F95F/41F97A|record210..220 /220..230|Four scalar stores,16 bytes each. RCX definitions survive the exact intervening stores. Fifth scalar is callee stack+28h / caller stack+20h; values not sampled.|
|46D110 at41F990/41F99C, tail202C70|record180..1C0 /1C0..200|Four sequential16-byte copies from original address01F204E0,64 bytes per call. **Copy, not zero-fill**; no general overlap claim.|
|3E5D00 at41FAFA|record4C0..510|WORD/DWORD/WORD,8 bytes per index. EDI is reset from zero ESI at41F9C0, then incremented and compared against10; exact indices0..9. Earlier EDI=FFFF is superseded. No arithmetic/MXCSR output or exception claim.|
|3E37E0 at41FB5A, tail861EC0|request record580..5D0|EDX=0,R8D=50h, named library fill. Its effects require the declared library contract; no stub or native effects fabricated.|

All helper footprints are inside740h and disjoint from WORD0 and DWORD284.
The complete supplied caller has125 direct nonstack w/rw spans. Full-width
intersection finds exactly one ID0 store (`41F795 WORD[RBX]=BP`); no direct store
overlaps284..288. LEA/address computations are excluded. The initial861EC0 call
requests zero fill over740h, before WORD0 is set toFFFF. Subsequent composed
effects do not change either protected field.

**Conditional normal-return result:** valid writable740h record, private
nonaliased frame, readable constant inputs, normal returns, standard fill
confined to its requested span, native ABI preservation and no interference
imply ID0=FFFF and active284=0 on return from41F730.

This removes the blanket unknown-helper-write premise for the supplied clear
chain. It does not prove native library implementation, arbitrary caller
validity, full all-writer closure, actual scene initialization, field atomicity,
ownership/reuse or lifetime. Exceptions/faulting memory/contaminated frames are
outside the normal-return proposition.

## Controls and reproduction

`prove-01.status.json`: actual CLI terminal0, driver
`b8ca12da919999a484c513d0f25ca080d6db1a0b9e96a7bd98c60acba7b06f85`.
`control-01.status.json`: actual CLI terminal0, driver
`cc1bff25acc7e682d95488067d3e8bf3bace765483a7325288240b8d0ce2c6a7`.
Five disposable actual producer refusals check failed capture, exception despite
exit0, incomplete wrapper, missing source and a coherently changed indexed
store address. Each must exit nonzero for its specific reason and emit no
result. Existing output is never accepted in place of a checked invocation.

Four labelled synthetic decoder/classifier controls use the reviewed adapter
and the exact producer functions: wide16-byte store starting278h intersects
active284; LEA at that start is address-only; DWORD read-modify-write at284 is
included; adjacent DWORD at280 ends exactly at284 and does not overlap.
These are regression controls, not additional shipping-code executions.

From a restored disposable copy of this packet in the repository, the existing
analysis venv can run `python -B prove.py fresh-result.json`. Result names must
be fresh. Reconstruct negative cases from `controls-01/*/input-identities.json`
using inherited base files plus retained overlays and explicit removals. Review
raw receipts and expected diagnostics, not merely the top-level verdict.

## Required consumer changes

OPUS: narrow the CharacterRenderRecord000/284 clear assumptions and the parent
slot initialization contract to the proved conditional result. Retain library,
ABI, valid extent, lifetime and scheduling qualifications.

FABLE: consume the same result in render allocation/system-clear and rig owner
sentinel preconditions. A fresh clear can establish empty ID/active values under
its explicit premises; it cannot establish natural caller/lifetime coherence.

SPEC: independently review original inputs/CFG/carriers/composition, actual
prerequisite path, full-width/RMW/address controls and the conditional wording.
Producer tests, external corroboration and independent acceptance are distinct.

Cleanup: every owned capture/proof/control process is terminal. Only owned
offline evidence files changed. No PC control, FF12 process, instrumentation,
saves, config, reference binaries or peer-owned consumer pages changed.
Historical four runtime-needs eliminations unchanged; zero whole OV rows closed.
Full L1+L2 goal remains ACTIVE/NOT_MET; EXP127 invalid, K14 closed, parked menu
allowance spent and extension unapproved.
