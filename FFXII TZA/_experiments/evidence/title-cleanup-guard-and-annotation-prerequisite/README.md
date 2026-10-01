# Conditional queued cleanup and source-reader qualification

2026-09-30, SOL in ASTRA. Producer checked; independent acceptance and canonical
incorporation pending. Method A STATIC_ONLY. No game or original-code execution.

## Question and method

Does zero DWORD object+BC prevent queued cleanup? Does the common cleanup path
honor a nonzero cleanup return, and what count/storage preconditions apply?
Competing explanations were a whole-cleanup guard versus a guard of the first
call only. Retained original code and complete normal unwind fragments suffice
to discriminate the local calls, stores and branches. Native effects, initialized
state and title lifetime require additional evidence and stay OPEN.

Shipping image SHA256 is
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, base120000.
Source records pin exact spans, raw bytes and reviewed access-role adapter.
62BCB0 needs five normal fragments, not only its65B root. Whole-table preparation
uses the PE Exception DataDirectory; a prior padding scan failed before output.

## Bounded findings

* 625F00 sets AL from DWORD+BC!=0. Ownership/refcount meaning and upper RAX are
  unproved.
* 5DE250 conditionally calls62BCB0, then normally tails616C60, which calls62BCB0
  unconditionally. Local direct-call multiplicity is one for sampled BC0, two
  for nonzero, assuming normal returns and excluding reentry.
* 62BCB0 delegates62B100, clears BC, then may delegate62B870 on pointer+20.
  Nonzero delegate EAX skips its record loop and is preserved. Ordinary loop
  completion writes EAX0. The outer callers do not test this result to abort.
* With post-delegate n=DWORD+30&7FFFFFFF, the loop bound is max(1,n). Storage
  selection is NULL for n0, inline+38 for n1, pointer[+38] for n>1; stride58B.
  Conditional loop-entry n0 produces the first read at absolute28. This is a
  state precondition/counterexample, not an observed game crash or proof that
  native delegates/constructors permit the state.
* 616C60 calls584730 only with bit31 clear, n>1 and pointer+38 nonNULL; every
  normal local branch then zeros+38/+30 and tails5DE290. Bit31 meaning beyond
  that predicate remains unassigned.

Native62B100/62B870/584730/5DE290, virtual callbacks, actual counts/storage,
all-child release, cancellation/drain, safe repetition and title lifetime remain
OPEN. Four consumer calls are not four frames; import metadata is not loaded CRT
behavior; no pointer/default/ownership guarantee is inferred.

## Actual reader defect and repair

The labelled original control changed the annotation at616C60 from PUSH RBX to
JE616CA7 while keeping bytes4053, span hashes and instruction counts. The legacy
reader exited0 and produced a result. That synthetic result is INVALID; retain
it as a reproducer. This establishes an unchecked annotation prerequisite, not a
wrong real disassembler decode or changed shipping instruction.

The current reader02 re-decodes every retained instruction and compares complete
operation/memory annotations through the shared reviewed adapter before CFG
reduction. The same false annotation now exits1 with no result. Missing normal
continuation and wrong unwind-parent controls also refuse. Result03 is the actual
nested-copy execution with the corrected adapter-location procedure; its bounded
semantic findings match result02. Result01 remains historical and its annotation
verification guarantee is superseded.

Publication's actual default preparation path now requires this consistency check
for the four pending tracker/queue/pump/import packets before creating destination
copies. Four retained prerequisites passed; changed annotation/role with updated
source pins, zero source map and missing source refused. These controls exercise
the actual prerequisite function and reader CLI. A real guarded prepare/publish
transaction is still required to certify the complete publication path.

Exact affected deliveries: title-tracker-callback-boundary,
title-queue-consumption, title-queue-pump-boundary, title-cleanup-import-boundary.
Their frozen inputs/results are unchanged. The pending readers omitted complete
annotation agreement; additive prerequisite receipts qualify that guarantee.
The positive re-decoding found no disagreement in their actual retained inputs.
This is not a regression claim about the canonical access index. No independent
acceptance, native execution or external audit is credited as producer testing.

## Reproduction and dependencies

In the same repository with Capstone5.0.7 and the shared reg_tracking.py SHA256
5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38, run
prove-title-cleanup-guard-scope-02.py with a fresh result path. The reader resolves
the actual ancestor repository adapter and rejects a moved dependency.
For the original false-annotation control pass
title-cleanup-annotation-prerequisite-control-01 as its optional source directory;
expect nonzero/no result. All source/case/result/exit receipts are retained.

The publication helper and control driver snapshots preserve the code reviewed
at the recorded run identity. Their full delivery controls additionally need the
four original frozen packets and current supported board; they are not a portable
mock of a publication transaction. Independent review must bind final inputs/code
and limits, not merely trust PASS text or manifest counts.

## Consumers and next discriminator

SPEC: independently review guard scope, count selector, abnormal-return boundaries
and the source-prerequisite repair. FABLE: incorporate accepted local facts and
qualifications through existing pages; route ABI/count/type consequences to OPUS.
Prior four packet reviews remain separate and pending.

Next inspect complete62B100/623DF0 and count/storage constructors or writers to
establish whether valid states exclude the zero-count witness. Prefer original
source/invariants; no parked menu attempt or EXP127 replay.

Cleanup: all invoked synchronous helpers terminal. No PC/input/instrumentation,
save/config/reference or peer changes. Full L1+L2/M0-M5 goal ACTIVE/NOT_MET.
