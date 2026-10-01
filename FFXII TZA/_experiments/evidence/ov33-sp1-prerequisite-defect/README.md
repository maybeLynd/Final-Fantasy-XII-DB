# Final v2 input binding and reproduction

The final driver uses explicit hash-checked immutable source and fixture inputs
and a fresh output argument. No mutable work-path defaults. Run03 executed that
actual invocation path from the prior frozen source and fixture bytes, terminal0
for the reproducer, with producer mismatch0 vs actual corrupt-parser refusal1.
This validates input binding; it is not extra scientific data or another corpus.

From repository root, use the pinned analysis Python:

    python <this-packet>/probe-sp1-prerequisite.py <this-packet>/run-03/original.py <this-packet>/inputs <fresh-owned-output-dir>

run-03/result.json pins the final driver/source/inputs, adaptation, exact child
statuses and exceptions. The supplied original-source copy remains unchanged.
Its legacy stdout phrase "peer source unchanged" means the supplied retained
source; it does not prove a current peer worktree was read during run03. Run02
alone checked the then-current original peer source. Neither proves game data
or semantics from a synthetic corpus. Earlier root driver in the v1 frozen
packet relied on mutable work defaults; that packet remains historical and is
not the final reproduction interface. Explicit inputs correct that cause.

# Returned OV33 SP1 producer: missing corpus is not success

Exact proposition: does failure of the required corpus detection control cause
a nonzero/incomplete producer result? Existing source suggests it prints only
MISMATCH and then FAILS0. Choose one actual offline subprocess counterexample,
not another full scientific census or any game setup.

Run02 reproduces the defect on pinned t1b_sp1_counts.py6cd80a4d...bd1701: only
the VBF input literal is adapted to a disclosed synthetic two-entry non-MPK
index. The real producer reports packs0/records0, CONTROL MISMATCH(0,0,0),
FAILS0 and exits0. A corrupt-magic index reaches actual load_index and refuses
with AssertionError/exit1. Original peer source stays unchanged. Retained
original/adapted drivers, input hashes, stdout/stderr and actual terminal status
are in run-02/result.json. Input fixtures are included byte-exact.

Run01 is INVALID: regex replacement interpreted Windows-path escapes, so both
children failed syntax checking before the producer ran. Its preliminary REJECT
wording and archive-control boolean are superseded, never semantic evidence.
Its original probe/source/output are retained. Fix: use a literal callback
replacement, and require the actual parser exception as the negative control.
Do not repeat the invalid adaptation. This is a reusable concrete-path lesson.

The actual original550-pack observations/count-max13 are not refuted by this
synthetic missing-corpus case. The defect blocks using terminal0/FAILS0 as proof
that prerequisites succeeded, and silent malformed-record omissions must be
made explicit. FABLE owns repair and downstream source/consumer changes;
ASTRA-CONTRA-FABLE-OV33-SP1-PREREQUISITE-0930 routes it once at40982. No duplicate
census or competing implementation. Nonauthor acceptance of the repair remains
required. No original FF12 execution, game, PC or saves/config access.
