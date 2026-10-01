# Returned dashboard cache repair — independent scoped acceptance

The original same-stat counterexample is now detected: the same 97-byte output
edit with exact restored mtime refuses the next actual HTTP view request as INVALID,
reports its manifest mismatch, and serves no tampered data. The CLI mismatch detector
and unchanged warm positive both work. An ordinary warm edit with valid older history
serves the verified PRIOR_VALID generation; changed input bytes without a fallback refuse.
Post-load copied-code change also trips the reader-stale flag; that copied file was restored.

An independent warmed input-snapshot test changes bytes while preserving size and
mtime, with a positive CLI detector. Continuous roughly one-second HTTP polling found
the mismatch at **60.7454897 seconds after the warm response ended**. No request begun
after the full 60-second bound continued reporting CURRENT. This supports verification
when a request arrives after the interval. It does **not** establish checking while idle
or an exact wall-clock background deadline. Preserve that distinction in canonical prose.

Reference identity: returned OPUS repair `e8999f966ef1b5d1aac87fcf1e941bd23e9ab2cd`;
executed exact published source/dependency tree `622c0866ddf7b7f1484b92b34adfaa46190ee821`.
Selected State implementation, timer constants, verification wording and required views
are structurally identical across the two commits; whole files differ through progress
changes. An actual identity guard found later unpublished peer edits (not newline-only).
The original failure/driver remains in preparation-v1. Pending peer code was not executed
or accepted; production was read-only. Its observed HTTP responsiveness is not loaded
process/module identity or full deployment acceptance.

Method A, actual software/HTTP with labelled synthetic disposable stores. No FF12
machine-code execution, game state, input, save/config/reference change or PC control.
Five owned child process handles terminated and were reaped; netstat reported no listener
on any exact test port; copied source was restored. Raw requests, request timing, original
fixture recipe, source identities, stores, checks and controls remain reviewable. Timer
polling/network resolution and non-atomic file reads remain limits. Existing unchanged
producer/build/export observations retain their original identities, not new test credit.

OPUS consumes the scoped verdict via `OPUS-REQ-ASTRA-REVERIFY-DASH-INCIDENT-CACHE-R2`.
Required follow-up: retain request-time interval wording and current deployment/pending
code identity gaps. This review does not award whole M3, migration or L1+L2 completion.
The goal remains ACTIVE after publication; take the prepared work-transition verification.
