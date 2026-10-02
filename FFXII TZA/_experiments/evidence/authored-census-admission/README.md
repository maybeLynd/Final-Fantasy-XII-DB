# Partial extraction is hidden by a positive sibling

This independent control directly enables the prepared OV42 authored-reference question for verbs 029A/029B. It tests the **research collector**, not the FF12 engine. No real archive, shipped bytecode, native/emulated FF12 code, game session or peer helper was changed or executed.

The committed `script_verb_census.py` is copied **unchanged** into three disposable project layouts. Its real `main()` and `census()` run. Only the input services are supplied by an explicitly fake `gen_req_channel_census` module: archive index/extractor, decoder, argument resolver, verb names and metadata. Synthetic section/directory/name bytes pass the real collector's container/directory/name checks; this does not validate the production decoder. The observer records attempted/returned/failed extractions and exact wrapper/collector identities.

| Labelled fixture | Actual observation |
|---|---|
| both members readable | CLI 0; two selected CALL rows, 029A and 029B |
| second extraction raises OSError | CLI 0; empty stderr; only first selected CALL row (029A); no failed-input/completeness field |
| both extractions raise | CLI 1; existing zero-CALL refusal; no output table |

The failed input is actually attempted; the wrapper's read-entry service raises and records it. The original collector catches that exception and continues. The all-failed control proves the zero-CALL check is active. A readable positive sibling bypasses that global zero condition, concealing the missing member. This is a concrete control-flow defect **if the result is used as complete corpus/absence evidence**; it does not establish that any historical real extraction failed.

Verdict: **REJECT as a standalone completeness/absence control**. A nonzero all-CALL count does not prove every relevant input was read, parsed or decoded. Previously captured positive callsites are not automatically invalidated. Universal absence/completeness consumers need explicit attempted/read/parsed/decoded/unresolved coverage and failure disposition, or independent complete-input evidence. The prepared DATA question must retain unknown cases. The helper also ignores the decoder's anomaly return at the source level; this control did not exercise that separate path and does not pretend it did.

OPUS owns the helper/contract repair; DATA owns the selected authored resource preparation. Options are a completeness-required mode that refuses/marks INCOMPLETE on failed relevant input, or explicit partial positive-only output with absence inference withheld. Do not change the unrelated OPUS partition implementation or repeat a whole corpus export for this control. After repair, use these exact fully readable, partial-failure and all-failed invocations to establish the intended policy.

`retention-01.json` binds the committed original driver and checkout agreement. `cases/*/status.json`, stdout/stderr, real emitted tables, fixture configuration/effects and driver copies preserve the actual invocation path. `result-01.json` is a deterministic reduction requiring all three terminal outcomes and the extraction positive/detection controls. The all-failed case is an expected refusal, not a zero-case semantic PASS. Reducer validity is not independent project acceptance.

All host children terminate. Their open fixture files close with process exit. No PC control remains active, no live-only claim closes, and the full L1+L2 goal stays active. Continue authored resource analysis at honest partial/complete scope while the owner repairs or specifies this collector's completeness contract.
