# Generation certification repair review — scoped REJECT

For the player: the export verifier now catches the previously found ambiguous or
malformed archives. One remaining metadata gap can still make it approve an archive
that omits a captured input. This is database-tool evidence, not an FF12 live test.

Question/consumer: does OPUS's shared admission parser refuse unknown input state
meaning as well as malformed structure? Exact published generation.py f145d442f is
retained with full revision, blob and SHA256 in run-01/raw.json. Method A: original
Python library and actual external CLI on disposable archive/folder copies. No
shipping FF12 code, running game, main producer reachability or current deployment.

The original97c4c1b65 positive/duplicate/unknownformat/malformedJSON ZIP bytes are
reused after original manifest SHA/size verification. New execution on repaired
code confirms the valid archive and refuses the original three defects. Additional
changed-parser controls refuse array manifest, wrong output container and nonstring
input state. A copied store's malformedJSON produces a reported problem rather than
exception; CLI status prints INVALID/exit1/no traceback (retained pointer hash also
disagrees, explicitly labelled). These supported fixes are not erased by the verdict.

Remaining counterexample: change exactly one present, nonexternal input's state to
ASTRA_LABELLED_UNKNOWN_STATE, retain all its other metadata, remove just its snapshot
member. The known-format archive now has one fewer member and still returns VERIFIED
in both library and actual CLI/exit0. The module documents only present, empty, missing
and unsupported. parse_manifest checks string type, but both membership paths skip
states other than present/empty. The unknown meaning silently removes an obligation.
This is a labelled invalid archive intervention; no claim that normal Store emits it
or that every unsupported/optional known state must be invalid.

Run `python -B check.py` here to validate retained evidence read-only. Its successful
exit supports a scoped rejection, not independent evidence acceptance. Reducer
controls must refuse incomplete/omitted positive/hidden VERIFIED observations.

All nine original CLI invocations are terminal, no stderr; library exception absent.
Actual verify-zip/status branches inspected: no children; self-test launch excluded.
No production board/store/controller/game/saves/config/reference change. No timeout
accepted, no earlier transition orphan cleanup inferred. Original settled export,
interruption/input campaigns not repeated. Full database and migration goal NOT_MET.

OPUS owns the parser/certification and affected current consumers. Preserve this
run, repair supported-state admission at the shared cause and re-request exact-source
review. Required own non-author evidence acceptance remains separate.
