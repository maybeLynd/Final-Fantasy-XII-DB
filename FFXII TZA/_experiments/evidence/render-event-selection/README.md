# Render event selection evidence

ASTRA, 2026-09-12. See [the canonical interpretation](../../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md).
This is an offline continuation of the capability-policy falsification, with no live
controls or new laboratory setup.

Hypotheses: a render event's selection depends on the caller's third argument; the
entry resolver has cache effects and address-width preconditions omitted by a pure
lookup oracle. Existing capability B omitted `004235C0`; the coast-down contract
supplied `0020E600` and `0051B9E0`. Distinguishing evidence is the complete caller/
callee constraint, cache writes, actual resource-bit reads and opposing policy results.

Method A: `primary.json`, `lookup.json`, `callers.json` record seven complete bodies
extracted from exact EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base `0x120000`.
They include Capstone 5.0.7 and function-extent source identity. `priority.json` is
the original 64-byte window at `01F00410`, not a declared full extent. Prior sealed
`efx-rebase-primary/primary.json` and `capability-policy-falsification` receipts supply
the reused provider/getter/predicate bodies; their exact hashes are in the new results.

Method B: the existing Unicorn 2.1.4 runner maps only verified shipping code and
injected data. The healthy cache/refresh feasibility pair completed first and is
preserved in `feasibility.json`. `result.json` has 24 valid original-code returns and
one separately invalid null-table case. `selection-controls.json` adds seven distinct
caller-policy controls; it does not rerun the prior suite. Eight bodies execute
without stubs; dependency reads, cache writes, stack/nonvolatile state and original
code bytes are checked. The 30,000-instruction limit and instruction whitelist stop
unexpected execution. No tagged provider path or event-entry caller is executed.

`review.py` reads all raw memory events and observed buffers independently; it replays
317 reads/four writes, verifies the opposed getter/selector result and actual bit-12
controls, and rejects a private receipt with a missing cache write. Successful return
flags cannot conceal that missing effect. Invalid or zero-case results cannot pass.
The negative invalid-state case is not counted as a successful return.

Data are constructed, not natively initialized. High-address refresh cases return
and cache pointers without dereferencing those payloads; they prove arithmetic/cache
effects, not that such a resource exists in gameplay. Getter simplification assumes
stable nonoverlapping records and successful dependency reads. Allocation, admission,
native lifetime, scheduling and integrated presentation remain open.

Reproduce from the repository root with the existing analysis Python environment.
The four `collect-*.py` scripts populate `Database/Tools/work/ASTRA/render-event-*.json`.
Place the preserved `probe.py` as `Database/Tools/work/ASTRA/render_event_probe.py`,
run its feasibility pair and preserve that receipt, then its main cases.
`selection-controls.py` records the reused instrument hash and executes only its
seven extra cases. `review.py` verifies both result files. The existing emulator
library needs scoped filesystem access; no game-process access is required.
Missing source identity, a failed control or an unexpected instruction/read stops
the affected case. `manifest.json` seals all files except itself.
