# Queued callback: original teardown and free import boundary

Method A only. Producer checked; independent acceptance pending. No native/game
execution, loaded CRT/IAT inspection, heap observation or natural title-state proof.

Player version: on normal return from its teardown helper, the queued cleanup
routine hands the original pointer to the C runtime's free function. The work
inside the teardown helpers, pointer validity and actual game lifetime remain open.

The exact question is the original boundary, not a promise that all resources
were safely freed.5DE25050B preserves input, calls625F00, conditionally calls62BCB0
when AL is nonzero, then tails616C60 with the pointer.17ECC0 calls that routine,
restores its own saved input to RCX on normal ABI return, then tails19C590.
Exact7B19C590 jumps through IAT8C2B48, whose original PE descriptor/lookup/name bytes
bind api-ms-win-crt-heap-l1-1-0.dll/free. It is not an object vtable dispatch.

Shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8;
reviewed adapter5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38
actually used with SSE-store/LEA/RMW controls, Capstone5.0.7. Exact source/import
metadata, local normal CFG, source gate/checker/helper hashes and CLI exits kept.
No larger body extent inferred for the7B tail lacking pdata here.

One checked positive reduction; three actual CLI refusals: missing source, wrong
import name and reversed teardown condition. Nonzero/no result each. Positive
reused, no fixture/native/live count or independent self-acceptance.

Preparation lessons: optional pefile unavailable before any output; bounded
stdlib PE parsing needs no install. First generated source had NUL/newline bytes
from escape replacement; the actual gate refused SyntaxError/exit1 before reading
an output. Two repair syntax preflights refused before new file/capture writes;
CRLF normalized in repair buffer and numeric byte replacement removed the escape
layers. Corrected02 compiled before invocation and passed. Invalid original bytes
are retained as history/bin plus failed raw receipt; no source/result01 exists.
Other packets have no dependency on this failed producer. Prefer literal file
patches and compile generated Python before writing/invoking it.

LIMITS:625F00/62BCB0/616C60 effects remain OPEN; no complete child-resource teardown,
cancellation/drain, leak/double-free safety, constructor state, pointer ownership,
reuse/thread or natural callback reachability guarantee. Named import metadata
is not loaded module identity or proof of an effect under a stub/modified IAT.
Normal callback/callee ABI return and valid native heap ownership are conditions.

Reproduce from repo root with fresh output:

    python <packet>/prove-title-cleanup-import-boundary.py <fresh-result.json>

Optional second argument selects disposable source copies for refusal controls.
SPEC reviews this new boundary; FABLE incorporates accepted title release prose,
routing OPUS-owned ABI/lifetime contracts once. Prior queue/caller/getter reviews
remain separate. Next inspect existing evidence for the three named teardown
callees and ownership prerequisites before new analysis/process observation.

Cleanup: own synchronous tools terminal; no PC/game/instrument/save/config/reference
writes. Parked menu spent/unapproved; EXP127 invalid. New wholeRT rows closed0,
cumulative retired1; full L1+L2/M0-M5 goal ACTIVE/NOT_MET.
