# Original render-removal branch and phase contracts

**Method A, STATIC_ONLY. Producer evidence, independent review/canonical
consumption pending. No FF12 instructions executed or live game used.**

Question: does non-NULL success from429140 imply an immediately free slot and
decreased count? When does active removal publish the count change relative to
native cleanup and clear? These affect the rendering lifecycle and observer
interpretation, not merely names or experiment coverage.

H1 treats success as immediate release and a coherent free-slot count. H2
distinguishes mark/no-op/pending-unlink-clear, with active count publication
before cleanup. Complete original bodies distinguish these source contracts;
natural scheduling/reentrancy requires separate evidence.

For the player: requesting removal of a displayed model and actually freeing
its rendering slot can happen at different stages. This package identifies
which paths mark it, clear it, or leave it unchanged.

## Reference and raw evidence

EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
base120000h. Captured full429140..4292A6 (358 bytes),427C90..427DD8 (328 bytes),
4200A0..4201EB (331 bytes):1017 original bytes. `source-01.json` contains original
bytes, decoded instructions and shared-reviewed memory roles. Actual capture
driver `130168736da06ffa0a3b8bb6b8cb6b393538977a40d80794f7da17197148e02d`;
capture01 terminal0 with raw stdout/stderr and interpreter identity.

`consumer-preimage.json` preserves the owning dual-list page at read. Its
accepted list/census corrections are retained; no new census performed.
`retained-clear/` binds the conditional clear result to immutable manifest
`c3e8141dc7fafc01b3fc7651abc3f5be49cf623f66e12c72b8a6615ef08439fc`.
At retention it was frozen/publication-ready, with producer validity and no
independent acceptance. This is reuse, not recapture or reexecution. Native
clear premises remain explicit.

## Branch meanings

Masks below are **numeric masks**, not bit numbers:284 mask04h is bit2;
290 mask01h is bit0;290 mask02h is bit1.

|429140 input/flags|Local result on normal return|Count / clear|
|---|---|---|
|NULL|return0|No dereference of the record, no helper calls or object writes|
|non-NULL,284 mask04 set|return1; mark: OR290 mask02, OR2AE mask01, zero108/110, clear284 mask04 and set bit30; call named binding/model helpers|No direct count decrement or41F730 call. Opaque effects separate.|
|non-NULL,284 mask04 clear,290 mask01 clear|return1, no helper calls or nonstack writes|No direct removal; record unchanged in this source path.|
|non-NULL,284 mask04 clear,290 mask01 set|return1 after pending-neighbor/end-point unlink and direct41F730 clear|Count decremented before clear; new count0 resets cursor. No4200A0 resource cleanup on this arm.|

Thus return1 alone does not certify immediate free-slot state. The no-op source
state model ID3/284=2010F9h/290=0 leaves the record unchanged and returns1.
That is a conditional input-state countermodel, **not evidence that normal
shipped gameplay reaches that combination**. All input memory must be valid.

For427C90, the active head at48800 supplies the selected row. The routine reads
dirty290 mask02 and caches signed next WORD4 in ESI before callbacks. Selected
removal repairs neighbor/end-point links and decrements count at427D18 before
42F4C0, optional child/owner cleanup and4200A0.4200A0 makes named resource/
embedded cleanup calls before its tail to41F730. The new-count0 cursor reset
also precedes cleanup. There is no source count-positive guard before either
selected DEC; the count comparison is after it.

These are instruction/order boundaries. They do not prove an atomic snapshot,
native helper effects, absence/presence of reentry, actual async observation,
finite child-chain progress or whole-system count/list/flags coherence. A
selected removal supplied count0 mathematically produces−1 and skips the
new-count0 reset; no native underflow or naturally corrupted state was run.

Active sweep does not test ID0 before dirty290 or count decrement. This supplies
a concrete qualifier for the page's universal “every consumer tests ID first”
wording. It does not reject the caller's possible valid-active-list invariant.

## Producer and controls

`prove.py` verifies current EXE, exact original bytes/entry populations, reviewed
annotations, all local CFGs (including4200A0's named tail), carrier/dominance,
four429140 predicate partitions and retained checked clear prerequisites before
writing an immutable result. Capstone register metadata is used only for
carriers; memory roles use the shared reviewed adapter.

Producer01 terminal0:
`4431e22ebe23e8f785fea3c11df00eea9332a7cba0f13b4985bbd48e95d66060`.
Control01 terminal0:
`26bd44ad2238ed19ad3a1c247af17c384cd3d7deed6b6403a9ebaac36f5cf389`.
Four actual disposable producer refusals: failed capture, incomplete wrapper,
missing retained clear result, coherently changed284 mask04→08. Each requires
terminal nonzero, its expected diagnostic and no result. Actual prerequisite
gates precede output. The four predicate partitions are source analysis, not
four original-code executions. Reuse settled full-width-role controls from the
clear parent; no repeated sample campaign.

In a restored disposable packet inside this repository, use the existing
analysis venv to run `python -B prove.py fresh-result.json`. Reconstruct each
negative CLI case from its `input-identities.json`, inherited base and retained
overlays/removals. Check actual receipt exit/exception and raw diagnostics.

## Consumer obligations and limits

FABLE: qualify dual-list removal prose around mask-controlled mark/no-op/clear,
count-before-cleanup phases and the ID-first statement. Preserve accepted
list-head/field/census corrections. Avoid claiming immediate lifetime release
from return1 or native effects from helper names.

OPUS: distinguish429140 return1 from “slot released”; preserve required valid
row/neighbors/list/count, normal ABI/returns and clear/library premises in
contracts. Capture phase labels must distinguish marking, count change and
successful final clear. All-writer/caller/lifetime/reentrancy closure stays open.

SPEC: independently derive the four branch partitions, normal-return values,
full native boundaries, caller carriers/order, actual prerequisite path and
qualified retained-clear use. A count/manifest match is integrity, not semantics.

No live initialization, allocation placement, original-code execution or
observed cleanup. No game/PC control/instrumentation/save/config/reference/peer
consumer changes. All owned bounded capture/proof/control processes terminal.
Historical four runtime-needs eliminations unchanged; zero whole OV rows
closed. Full L1+L2 goal ACTIVE/NOT_MET; K14 closed, EXP127 invalid, menu allowance
spent and extension unapproved.
