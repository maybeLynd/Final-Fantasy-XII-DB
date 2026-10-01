# Typed-pop tag and reporting boundary

ASTRA, method A. This package reads exact shipping instructions and a current
canonical consumer. No guest/native/live execution, invented callback return,
copied game EXE, or valid comparison sample replay was performed.

Question: does the EC7-98 paragraph in
`01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`
correctly describe `00267E60`'s float conversion tag and empty-pop reporting?
It says `cvtdq2ps` applies to tag3 and `008620C0` raises on empty pops.
The original code is sufficient to distinguish conversion of tag1 vs tag3,
both-arms reporting vs asymmetric reporting, and an exception/termination call
vs a retail returning no-op. FABLE owns semantics/prose; OPUS owns contracts.

## Identity and controls

Certified EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base
`00120000`. Exact bodies: typed pop `00267E60` 256B, reporting wrapper
`008620C0` 14B, folded return `0016D6A0` 3B. Full bodies are retained; their
individual hashes and physical instruction/access rows are in `raw.json`.
Current page copies carry content/Git identity, not an asserted independent
acceptance. `capture-terminal.json` records the successful capture's real status.

The previously verified shipping reader's unchanged `load_image`/`img_rd` were
AST-extracted, with the same certified image at the repo reference pathname;
its full original source was retained and Git-byte-verified. Its unrelated
Unicorn harness was not imported/run. The shared reviewed access-role adapter
is called in the actual capture and independent decoding paths. Driver,
Python/Capstone/provider identities, initial evidence identity, source unchanged
checks and selected original bytes are retained. The pre-existing `check.py`
was an identity-only gate, not semantic acceptance; its original bytes are
preserved in `check-initial.py`. The final read-only semantic reducer and its
actual positive/three alternative-refusal statuses are separate receipts.

## Original branch facts

After `00262440` supplies the temporary record, `00267E84` reads its kind at
`[rsp+0x34]`. Subtracting1 selects the kind1 arm when zero; for kind2 it leaves
`r8d=1` and selects the float arm.

In that float arm, positive depth is decremented and stored before the tag
test. The byte at `stack+4+index` is loaded at `00267EA9`, then `sub ecx,r8d`
normalizes it by1. The zero branch enters `00267EC9` `movd` and `00267ED2`
`cvtdq2ps`. Thus **tag1 converts the signed integer**. A normalized1 (original
tag2) uses `movss` to copy float bits. Other tags, including3, branch to
`00267EE7` and write zero float bits to `[rsp+0x50]`. These are conditional
source branch calculations, not newly executed tag cases or native FP results.

For **kind2** depth<=0, `00267EA0` jumps to `00267EDD`; it calls the reporter at
`00267EE2` then writes zero float bits. For **kind1** depth<=0, `00267EF6` jumps
straight to `00267F18`, skips the reporter, and writes integer0. This is an
asymmetric reporting boundary. The kind1 bad-tag arm does call the reporter
at `00267F13`, after consuming the entry; it is different from empty input.

The reporting wrapper's complete instructions are `lea rdx,string`,
`xor ecx,ecx`, `jmp 0016D6A0`; the target's complete bytes are `C2 00 00`,
`ret 0`. No call to a message emitter, throw, process exit, memory write or
display occurs in these two bodies. This is original code, not a replacement
stub assumed to return. The reporting call stages/drops a string and returns.

The reducer pins original branch instructions and decodes them independently.
It refuses three concrete wrong interpretations: tag3 converts, both underflow
arms report, and the reporting leaf terminates. Those are source/refusal controls,
not additional original-code experiments or external audit executions.

## Consequences and limits

The consumer paragraph needs tag3->tag1 and precise underflow/reporting wording.
The already existing interpreter-page no-op description is supported at this
instruction boundary. No whole ScriptVM question or package acceptance follows.

**Zeros here are written into the temporary value record at `[rsp+0x50]`;
they are not proved final function return values.** The remainder may call
`0032F240` and does call `0026D530`. Their effects, `00262440` record binding,
actual initialization, lifetime, native caller reachability, malformed authored
scripts and visible behavior were not executed or proved here. A failed or
corrupted caller can have consequences outside this exact returning report
chain. The no-op alone is not evidence of general malformed-input safety.

Consumer incorporation remains pending until the authorized owner updates all
affected current claims and agrees on scope. Required non-author review is
separate. Original page snapshots stay immutable. No peer source edits,
process/instrument/control session, save/config change or cleanup were needed;
all owned calls are terminal. The menu's spent allowance/unapproved extension
and required live-only gaps remain. Full L1+L2 goal stays ACTIVE, NOT_MET.

Player version: this helper's error-report path does not stop retail game code.
For this exact branch, a missing value writes zero into a temporary record;
that does not establish what a malformed gameplay script would ultimately do.
