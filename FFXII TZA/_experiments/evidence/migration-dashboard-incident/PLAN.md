# Independent dashboard incident verification — SOL in ASTRA

Request: OPUS-REQ-ASTRA-VERIFY-DASH-INCIDENT, claimed at current epoch3/rev38741.
Governing migration: FF12-WORKFLOW-MIGRATION-20260928-01; A05–A09/A17/A19
incident subset, not whole migration M0–M5 or whole database acceptance.
Owner OPUS; deployment FRONTIER; verifier SOL/ASTRA, no production coauthorship.

Competing explanations: the deployed reader correctly distinguishes external
inputs and refuses incoherent output, versus a stale reader/unchecked candidate/
cache/cutover allowing an apparently certified incoherent generation. No game
or native FF12 code is needed. Method A: actual tooling and real loopback HTTP,
synthetic disposable fault stores explicitly separate from deployed observations.

Cases derived from the request and policy before reading producer test files:

1. Deployed HTTP status plus seven views bracketed by status reads: identify
   served/current generation, stale reasons, failure record, code-stale flag;
   mixed generations fail the coherence assertion (one bounded retry only for
   an observed cutover). This is a current deployment observation, not mock parity.
2. Actual Store/CLI and actual server subprocess on small controlled snapshots:
   valid ordinary and external input, seven valid view sentinels, passes baseline.
3. Corrupt a real snapshotted input and a real output, before first read and after
   a warm reader cache. Invalid current must not serve corrupted bytes. Verified
   older fallback is acceptable only explicitly HISTORICAL. No older valid state
   means no data, not zero/green. Include same-length content edit with restored
   mtime to distinguish fingerprint guarantees from a stat-only invalidation key.
4. A missing required output/changed strict input refuses a build, keeps exact
   previous CURRENT bytes, records failure separately, and creates no success
   history for the failed candidate. Output data/content controls, not exit alone.
5. Mutate a disposable volatile board after snapshot but before commit: snapshot
   must remain coherent, strict drift still rejects. Run the real build_views.py
   CLI once into an exclusive scratch root; preserve exits/raw status and compare
   authoritative board revisions around it. Do not rebuild or alter the live store.
6. Unknown manifest format yields UNSUPPORTED/explicit unsupported detail, no
   certification based on guessed format. Change only a private server/module
   source after its process loads, then require reader_stale=true over actual HTTP.
7. Controls with ordinary byte tamper and valid empty/failure-free baseline keep
   negative claims connected to a functioning detector. Read-only HTTP behavior
   and actual loopback binding are observable subprocess controls, not a GUI test.

Budgets: <=5s/request, <=12s startup, <=120s normal build before explicit timeout;
one process per private server at a time; no production restart/stop, live-store
write, controller changes, FF12, save/config/reference mutation or tool installation.
Always stop/wait private child servers in finally; timeout/nonzero/missing result
is incomplete/failure, never PASS. Retain source copies/hashes, driver, raw HTTP,
CLI output/status, fixture paths/content identities, normalized checks and cleanup.

Source inspection occurred only after deriving the above requirement questions;
producer test files are not yet read. Initial read-only feasibility HTTP responded
with g20260929T021909Z-915e26, all seven STALE due to a moved package, not a green
current-data claim. Claim wait completed normally; no guard/lock bypass/replay.
Stop when each discriminator is settled; do not manufacture more counters.

Limits: scratch tests are synthetic tooling fixtures, not gameplay or whole-host
or controller parity. A real scratch CLI build is not deployment cutover. Current
runtime/menu budget restrictions persist; PC control OFF; DB_GOAL=NOT_MET.
