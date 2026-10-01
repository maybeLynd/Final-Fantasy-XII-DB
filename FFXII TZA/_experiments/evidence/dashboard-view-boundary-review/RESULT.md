# Independent delta-basis boundary finding

Target: OPUS delivery `eae0ed3c7d1ed9f8f41a401b85e1fedb4ed39cc9`, review
`OPUS-REQ-ASTRA-VERIFY-DASHBOARD-VIEWS-0929-R`.

The exact pinned production `M`, `annotate_deltas`, `check_view` and `_states`
functions were executed on six bounded host fixtures. All twelve input views
passed that delivery's real view validator. Git extraction exits and nonempty
sources were checked. Python 3.14.6; probe terminal exit **1**, not PASS.
`zero-basis-result.json` preserves each prior/current view, validation result,
source hashes, observations and the six requirement checks.

Controls succeeded: count 10 -> 15 gives count +5 / relative +50%; ratio
10/100 -> 15/200 gives dnum +5 and dden +100 without pp; changed scope refuses
a numeric count delta.

The discriminator failed: prior 0/0 -> current 5/null at the same definition,
id and scope gives a numeric count +5, rewrites the prior denominator to null,
and supplies no basis-change refusal. Prior 1/2 -> current 0/0 also rewrites
the current denominator to null; unchanged 0/0 loses both zero denominators.
The actual producer's `if not m.get("denominator")` and old-denominator
truthiness conflate zero with null. Schema and production validation allow
0/0; it is not a malformed fixture. No universal occurrence in current tiles
is claimed: this is a demonstrated admitted contract boundary defect.

Disposition: **REJECT the delivered like-for-like delta boundary**, with other
requested build/server/VBF/evidence/seal acceptance pending. Consumer OPUS:
distinguish null plain counts from zero ratios, preserve actual old/new bases,
and refuse numeric count/rel/pp across a ratio/count change. Add focused tests
to the real invocation path for these three failures, retaining the ordinary
count, moved-ratio and changed-scope positives. A zero ratio must not divide by
zero or have its basis erased. Definition versions alone cannot excuse an
accepted same-version input being silently rewritten.

Limits: exact production host function slices, not the full build/server,
installed archive run, game execution, whole workflow acceptance or FF12
semantics. AST extraction omits unrelated module initialization; no conclusions
about it are made. Current peer files remain untouched. No live process,
browser, instrumentation, saves/configuration or reference binary was used.
Fixtures are disposable own work; retained source/input/result receipts are
immutable. No unchanged rerun is needed. Reproduce into a **fresh owned
directory**, using a copy of the driver: it refuses overwritten inputs/results.

Player version: the dashboard can confuse “nothing in this measured group”
with “a simple count,” then show a misleading progress change. This finding
requires a dashboard fix, not another game experiment.
