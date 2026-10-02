# Route-2 cache commit: key provenance

Exact question: at the supplied original resolver's 59F1B7 -> 59A9B0 ->
59AAA4 -> 1D6A20 path, is the insertion key recomputed from the archive path,
or carried from the previous cache lookup's record+28 out-parameter? Does an
empty normalized lookup initialize that out-parameter?

H1: every armed cache fill freshly computes/masks its insertion key.
H2: the commit forwards record+28; the nonempty lookup writes a 31-bit hash,
but the empty-normalized return does not write the out-parameter.
Major system: resource/cache source binding; OV33 E2 input-domain prerequisite.
Consumers: FABLE path-resolution/cache page, OPUS source-record/ABI contracts.

Method A: original complete local CFGs 59EE90 through RET59F1FB, 59A9B0 and
20C1B0. Reuse accepted original 1D6D20 and 674A00 bytes, not the normalizer's
seven illustration samples, the selector/filter census or archive export.
Prior pc1-config-route and current path/FST pages cover routing/commit roles;
they do not settle this out-key provenance boundary. Cheapest sufficient
method is static carrier/branch proof with a small finite r12b reachability
analysis. B execution cannot establish native aliasing or natural caller inputs;
C is unnecessary for these conditional code rules. No game setup.

Observe exact 59F1B0 EDX=[record+28], saved ESI -> ECX in 59A9B0, argument5
through 1D6D20 to R14, hash return store20C22D and empty branch20C21D.
Prove armed commit cannot be locally reached without the lookup call under
Win64 nonvolatile-register ABI; prove all hash exits clear bit31. Keep conditional
stable state/no-interference/valid record/nonalias/private stack/readable terminated
normalizer buffer/normal returns premises. Pointer carrying is not memory stability.
The empty case is a qualified retained-value boundary, not evidence a shipped
archive hit or normal game invocation uses an empty name or a high-bit key.

Acceptance: exact source/binary/shared-role/terminal status checks precede result;
complete local CFG/carrier/value gates plus discriminating coherent-byte and
upstream failure controls. Capture includes the resolver's actual epilogue beyond
the prepared .pdata range ending59F1E2. Do not infer extent from a fragment alone.
Invalidation: missing input, partial/failed invocation, incoherent source, unknown
carrier write or unaccounted local edge refuses output. No valid-empty PASS.

Cleanup: bounded own offline children terminal; no FF12, UI, saves, configuration,
reference binaries, peer files/cache or process changes. Freeze driver/source/case/
result receipts, publish under brief supported reservation, route independent
SPEC and FABLE/OPUS incorporation once. Producer validity is not independent
acceptance. New natural/lifetime questions remain separately open.

Learned preconditions: no local inspect.py; shared reviewed memory-role adapter
must run in the actual capture and reader. Call success/output presence do not
supersede exit/exception/completion. Preserve failed hypotheses and preimages.
